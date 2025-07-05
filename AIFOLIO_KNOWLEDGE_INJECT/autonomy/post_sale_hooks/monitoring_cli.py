import argparse
from autonomy.post_sale_hooks.monitoring import replay_failed_hooks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay failed post-sale hooks.")
    parser.add_argument(
        "--replay", action="store_true", help="Replay all failed post-sale hooks"
    )
    args = parser.parse_args()
    if args.replay:
        replay_failed_hooks()
    else:
        print("No action specified. Use --replay to replay failed hooks.")
