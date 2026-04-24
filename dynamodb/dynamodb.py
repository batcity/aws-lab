import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('users')
table.delete()

table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'last_name',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'last_name',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.wait_until_exists()

table.put_item(
    Item={
        'username': 'complex_put_query',        # Partition Key (String)
        'last_name': 'complex',        # Sort Key (String)
        
        # --- Scalars ---
        'age': 30,                 # Number
        'is_active': True,         # Boolean
        'description': None,       # Null
        
        # --- Sets (Unique values only) ---
        'tags': {'python', 'aws'}, # String Set
        'lucky_numbers': {7, 11},  # Number Set
        
        # --- Documents (Nested) ---
        'metadata': {              # Map (Dictionary)
            'login_count': 5,
            'last_login': '2026-04-24T17:15:00Z',
            'devices': ['iPhone', 'MacBook'] # List (Array) inside a Map
        },
        'history': [               # List of Maps
            {'event': 'signup', 'date': '2026-01-01'},
            {'event': 'upgrade', 'date': '2026-03-15'}
        ]
    }
)

table.put_item(
   Item={
        'username': 'jdoe',
        'last_name': 'Doe',
        'profile_details': { # This nested Map makes it a "document"
            'age': 30,
            'interests': ['coding', 'hiking'],
            'address': {
                'city': 'Seattle',
                'state': 'WA'
            }
        }
    }
)

table.put_item(
   Item={
        'username': 'test',
        'last_name': 'kim',
        'profile_details': { # This nested Map makes it a "document"
            'age': 33,
            'interests': ['coding', 'podcasts'],
            'address': {
                'city': 'Los Angeles',
                'state': 'CA'
            }
        }
    }
)

# Print out some data about the table.
print(table.item_count)