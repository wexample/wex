#!/usr/bin/env python3
import click
from src.core.Kernel import Kernel


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = kernel


if __name__ == '__main__':
    kernel = Kernel()
    kernel.call(cli)
