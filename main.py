import argparse

from MyTracert import MyTracert


def main(address: str, max_steps: int, timeout: int):
    mytrcrt = MyTracert(address, max_steps, timeout)
    return mytrcrt.tracert_run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Traceroute utilit"
    )
    parser.add_argument(
        "domain_name", type=str, help="what address to trace"
    )
    parser.add_argument(
        "max_steps", type=int, help="maximum number of steps to go"
    )
    parser.add_argument(
        "timeout", type=int, help="maximum number of steps to go"
    )

    args = parser.parse_args()

    main(
        args.domain_name,
        args.max_steps,
        args.timeout,
    )
