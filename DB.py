import supabase

supabase_url = 'https://xsqxdgtmmlfjubodeinc.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhzcXhkZ3RtbWxmanVib2RlaW5jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc0MjI4MjYsImV4cCI6MjAyMjk5ODgyNn0.tDnhgypAgUx4XL1pN9KLvQqY4QjfxjRZYD0VDX845cI'
client = supabase.create_client(supabase_url, supabase_key)

def fetch_lasertag_data_by_name(name):
    # Fetch data from the "LaserTag" table based on the provided name
    response = client.from_('LaserTag').select('ID, Name, Team, Score').eq('Name', name).execute()

    # Check if data is available
    if response.data:
        lasertag_data = response.data
        print('LaserTag data:', lasertag_data)
    else:
        print('No data found for name:', name)
        create_new_entry(name)

def create_new_entry(name):
    # Prompt the user to create a new entry
    print('No existing entry found for name:', name)
    print('Please create a new entry:')
    new_id = input('Enter ID: ')
    new_team = input('Enter Team: ')

    # Insert new entry into the table with score set to 0
    data = client.table('LaserTag').insert([{
        'ID': int(new_id),
        'Name': name,
        'Team': int(new_team),
        'Score': 0
    }]).execute()

    print('New entry created successfully.')

# Prompt the user to enter their name
name = input('Enter your name to fetch or create data: ')

# Call the function synchronously
fetch_lasertag_data_by_name(name)
