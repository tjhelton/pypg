#!/usr/bin/env python3
"""
SafetyCulture Template Access Rules Export Script

This script exports all permission assignments for each template in a SafetyCulture environment.
It retrieves data from the templates, users, and groups datafeeds and generates a CSV report
showing individual permission assignments for each template.

Output CSV columns:
- template_id: The unique identifier of the template
- name: The name of the template
- permission: The type of permission (view, edit, delete, owner)
- assignee_type: Whether the assignee is a 'user' or 'group'
- assignee_id: The UUID of the user or group
- assignee_name: The display name of the user or group
"""

import csv
import sys
from typing import Dict, List, Optional, Generator

import requests

# Configuration - Replace 'your_token_here' with your actual SafetyCulture API token
TOKEN = ''  # Add your API token here
BASE_URL = 'https://api.safetyculture.io'


class SafetyCultureClient:
    """Client for interacting with the SafetyCulture API"""

    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def _make_request(self, url: str) -> dict:
        """Make a GET request and return JSON response"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error making request to {url}: {e}")
            raise

    def _transform_feed_id(self, feed_id: str) -> str:
        """
        Transform feed ID from format 'role_6e628f054e904d5a9692535246beecb8'
        to proper UUID format '6e628f05-4e90-4d5a-9692-535246beecb8'
        """
        if '_' not in feed_id:
            return feed_id

        # Split on underscore and take the second part
        uuid_part = feed_id.split('_')[1]

        # Convert to proper UUID format (8-4-4-4-12 characters)
        if len(uuid_part) == 32:  # 32 character hex string
            formatted_uuid = f"{uuid_part[:8]}-{uuid_part[8:12]}-{uuid_part[12:16]}-{uuid_part[16:20]}-{uuid_part[20:]}"
            return formatted_uuid

        return uuid_part

    def fetch_paginated_feed(self, endpoint: str) -> Generator[dict, None, None]:
        """Fetch all records from a paginated datafeed endpoint"""
        url = f"{self.base_url}{endpoint}"

        while url:
            print(f"  Fetching: {url}")
            response = self._make_request(url)

            # Yield each item in the data array
            yield from response.get('data', [])

            # Get next page URL from metadata
            metadata = response.get('metadata', {})
            next_page = metadata.get('next_page')

            if next_page:
                url = f"{self.base_url}{next_page}"
            else:
                url = None

    def get_template_by_id(self, template_id: str) -> Optional[dict]:
        """Get detailed template information by ID"""
        url = f"{self.base_url}/templates/v1/templates/{template_id}"
        try:
            response = self._make_request(url)
            return response.get('template')
        except requests.RequestException:
            print(f"  Warning: Could not fetch template {template_id}")
            return None


def process_template_permissions(template: dict, users_lookup: Dict[str, str],
                               groups_lookup: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Process template permissions and return list of permission records.
    Each record represents one permission assignment.
    """
    records = []
    template_id = template.get('id', '')
    template_name = template.get('name', '')
    permissions = template.get('permissions', {})

    # Process each permission type (view, edit, delete, owner, context)
    for permission_type, permission_list in permissions.items():
        if not isinstance(permission_list, list):
            continue

        for permission_entry in permission_list:
            assignee_id = permission_entry.get('id', '')
            permission_obj_type = permission_entry.get('type', 'USER')

            # Determine assignee type and name
            if permission_obj_type == 'ROLE':
                assignee_type = 'group'
                assignee_name = groups_lookup.get(assignee_id, f'Unknown Group ({assignee_id})')
            else:  # USER
                assignee_type = 'user'
                assignee_name = users_lookup.get(assignee_id, f'Unknown User ({assignee_id})')

            records.append({
                'template_id': template_id,
                'name': template_name,
                'permission': permission_type,
                'assignee_type': assignee_type,
                'assignee_id': assignee_id,
                'assignee_name': assignee_name
            })

    return records


def write_csv_header(csv_writer):
    """Write CSV header row"""
    csv_writer.writerow([
        'template_id',
        'name',
        'permission',
        'assignee_type',
        'assignee_id',
        'assignee_name'
    ])


def _fetch_users_lookup(client):
    """Fetch and build users lookup table"""
    print("\\n1. Fetching users...")
    users_lookup = {}
    user_count = 0

    for user in client.fetch_paginated_feed('/feed/users'):
        user_id = user.get('id', '')
        user_name = f"{user.get('firstname', '')} {user.get('lastname', '')}".strip()
        if not user_name:
            user_name = user.get('email', 'Unknown User')

        # Transform the ID format
        transformed_id = client._transform_feed_id(user_id)  # pylint: disable=protected-access
        users_lookup[transformed_id] = user_name
        user_count += 1

        if user_count % 100 == 0:
            print(f"  Processed {user_count} users...")

    print(f"  Completed: {user_count} users loaded")
    return users_lookup


def _fetch_groups_lookup(client):
    """Fetch and build groups lookup table"""
    print("\\n2. Fetching groups...")
    groups_lookup = {}
    group_count = 0

    for group in client.fetch_paginated_feed('/feed/groups'):
        group_id = group.get('id', '')
        group_name = group.get('name', 'Unknown Group')

        # Transform the ID format
        transformed_id = client._transform_feed_id(group_id)  # pylint: disable=protected-access
        groups_lookup[transformed_id] = group_name
        group_count += 1

        if group_count % 50 == 0:
            print(f"  Processed {group_count} groups...")

    print(f"  Completed: {group_count} groups loaded")
    return groups_lookup


def _process_templates(client, users_lookup, groups_lookup, csv_writer, csv_file):
    """Process templates and write permission records"""
    print("\\n3. Processing templates and permissions...")
    template_count = 0
    records_written = 0

    for template_summary in client.fetch_paginated_feed('/feed/templates'):
        template_id = template_summary.get('id', '')

        # Skip archived templates
        if template_summary.get('archived', False):
            continue

        # Get detailed template information
        template_detail = client.get_template_by_id(template_id)
        if not template_detail:
            continue

        # Process permissions for this template
        permission_records = process_template_permissions(
            template_detail, users_lookup, groups_lookup
        )

        # Write records to CSV in real-time
        for record in permission_records:
            csv_writer.writerow([
                record['template_id'],
                record['name'],
                record['permission'],
                record['assignee_type'],
                record['assignee_id'],
                record['assignee_name']
            ])
            records_written += 1

        csv_file.flush()  # Ensure data is written immediately

        template_count += 1
        if template_count % 10 == 0:
            print(f"  Processed {template_count} templates, {records_written} permission records written")

    print("\\n Export completed!")
    print(f"   Templates processed: {template_count}")
    print(f"   Permission records: {records_written}")
    return records_written


def main():
    """Main function to export SafetyCulture template access rules"""
    if TOKEN == 'your_token_here' or not TOKEN:
        print("Error: Please set your SafetyCulture API token in the TOKEN variable")
        return 1

    print("SafetyCulture Template Access Rules Export")
    print("=" * 50)

    client = SafetyCultureClient(BASE_URL, TOKEN)
    output_file = 'template_access_rules.csv'

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            write_csv_header(csv_writer)
            csv_file.flush()

            # Fetch all users and build lookup table
            users_lookup = _fetch_users_lookup(client)

            # Fetch all groups and build lookup table
            groups_lookup = _fetch_groups_lookup(client)

            # Process templates and write permission records
            records_written = _process_templates(client, users_lookup, groups_lookup, csv_writer, csv_file)
            print(f"   Output file: {output_file}")
            print(f"   Total records written: {records_written}")

    except (requests.RequestException, ValueError, IOError) as e:
        print(f"\\nError during export: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
