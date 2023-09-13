#!/usr/bin/python3
'''
This module defines the REST API
'''
import json
import requests
from sys import argv    
BASE_URL = 'https://jsonplaceholder.typicode.com'


def get_username(id):
    '''Fetch employee username by ID'''
    response = requests.get(f'{BASE_URL}/users/{id}')
    response.raise_for_status()
    user_data = response.json()
    return user_data.get('username')


def get_todos(id):
    '''Fetch TODOs for the given employee ID'''
    response = requests.get(f'{BASE_URL}/todos', params={'userId': id})
    response.raise_for_status()
    return response.json()


def export_to_json(id):
    '''Export the TODO list to JSON for the given employee ID '''
    try:
        employee_username = get_username(id)
        todos = get_todos(id)

        tasks_list = []
        for task in todos:
            task_data = {
                "task": task['title'],
                "completed": task['completed'],
                "username": employee_username
            }
            tasks_list.append(task_data)

        # Construct the final JSON structure
        json_structure = {str(id): tasks_list}
        with open(f"{id}.json", "w") as json_file:
            json.dump(json_structure, json_file)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(argv) < 2:
        exit(1)

    employee_id = int(argv[1])
    export_to_json(employee_id)
