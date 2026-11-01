# !/usr/bin/env python3
import argparse
from cropsflow import CropsFlow
from designer_agent.agents import TaskDesignerAgent


def main():
    parser = argparse.ArgumentParser(description='A simple CLI tool')
    parser.add_argument('name', help='Your name')
    parser.add_argument('-a', '--age', type=int, help='Your age')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")

    print(f"Hello, {args.name}!")
    if args.age:
        print(f"You are {args.age} years old.")
    CropsFlow.start(TaskDesignerAgent)


if __name__ == '__main__':
    main()
