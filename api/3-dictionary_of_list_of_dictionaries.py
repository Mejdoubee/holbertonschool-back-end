#!/usr/bin/python3
'''
Export data in JSON format for all employees.
'''
import json
import requests

BASE_URL = 'https://jsonplaceholder.typicode.com'


def get_users():
    '''Fetch all users'''
    response = requests.get(f'{BASE_URL}/users')
    response.raise_for_status()
    return response.json()


def get_todos(user_id):
    '''Fetch TODOs for the given user ID'''
    response = requests.get(f'{BASE_URL}/todos', params={'userId': user_id})
    response.raise_for_status()
    return response.json()


def export_all_to_json():
    '''Export the TODO list for all employees to JSON'''
    all_users_data = {}

    try:
        users = get_users()
        for user in users:
            user_id = user['id']
            username = user['username']
            todos = get_todos(user_id)

            tasks_list = []
            for task in todos:
                task_data = {
                    "username": username,
                    "task": task['title'],
                    "completed": task['completed']
                }
                tasks_list.append(task_data)

            # Construct the final JSON structure
            all_users_data[str(user_id)] = tasks_list

        with open("todo_all_employees.json", "w") as json_file:
            json.dump(all_users_data, json_file)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    export_all_to_json()
