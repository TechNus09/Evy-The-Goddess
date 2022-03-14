from typing import Callable, Coroutine
from functools import wraps
from interactions import (
    CommandContext as sctx,
    Permissions,
)

def say(ctx,msg):
    ctx.send(msg,ephemeral=True)



def check(predicate: Callable[..., bool]):

    def decorator(func: Coroutine):

        @wraps(func)
        async def wrapper(self, ctx: sctx, *args, **kwargs):
            if predicate(self, ctx):
                return await func(self, ctx, *args, **kwargs)
            else:
                await say(
                        ctx,
                        f"Check for command {ctx.data.name} has failed.")

        return wrapper

    return decorator


def is_owner(arg=None):

    def predicate(self, ctx: sctx):
        return int(ctx.author.id) in self.bot.owner_ids

    if callable(arg):
        return check(predicate)(arg)
    else:
        return check(predicate)


def has_permissions(*permissions: Permissions):

    def predicate(self, ctx: sctx):
        for permission in permissions:
            if ctx.author.permissions & permission != permission:
                return False
        return True

    return check(predicate)