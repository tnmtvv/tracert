import argparse

from MyTracert import MyTracert


def main(address, max_steps):
    mytrcrt = MyTracert(address, max_steps)
    return mytrcrt.run()


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

    args = parser.parse_args()

    main(
        args.address,
        args.max_steps,
    )
