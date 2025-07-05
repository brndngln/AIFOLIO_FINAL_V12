import os
import argparse

FAILED_HOOKS_LOG = "logs/failed_hooks.log"


def replay_hook_line(line):
    # Parse log line to extract hook name and args (stub)
    print(f"[REPLAY] Would replay: {line.strip()}")
    # TODO: Actually invoke the hook with parsed args


def main():
    parser = argparse.ArgumentParser(description="Replay failed post-sale hooks.")
    parser.add_argument("--hook", type=str, help="Replay only this hook name")
    parser.add_argument("--all", action="store_true", help="Replay all failed hooks")
    parser.add_argument("--filter", type=str, help="Filter log by keyword")
    args = parser.parse_args()
    if not os.path.exists(FAILED_HOOKS_LOG):
        print("No failed hooks log found.")
        return
    with open(FAILED_HOOKS_LOG) as f:
        lines = f.readlines()
    for line in lines:
        if args.hook and args.hook not in line:
            continue
        if args.filter and args.filter not in line:
            continue
        if args.hook or args.filter or args.all:
            replay_hook_line(line)
    if not (args.hook or args.filter or args.all):
        print("Specify --hook, --all, or --filter to replay.")


if __name__ == "__main__":
    main()
