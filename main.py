class Client:
    def __init__(self, **options):
        self.timeout = options.get('timeout', 30000)
        self.webhook = options.get('webhook', None)
        self.actions = options.get('actions', [])

    def add_action(self, action):
        self.actions.append(action)

    def __getattr__(self, item):
        return Action(item, client=self)


class Action:
    def __init__(self, action, args=None, client=None):
        if args is None:
            args = []
        self.action = action
        self.args = args
        self.client = client

    def __getattr__(self, item):
        return Action(f'{self.action}.{item}', client=self.client)

    def __call__(self, *args, **kwargs):
        self.args.extend(args)
        self.client.add_action(self)
        return self

    def to_dict(self):
        return {
            "action": self.action,
            "args": self.args,
        }


# Usage:
context = Client()

action3 = context.browser.page.goto("https://google.com")
print(action3.to_dict())  # {'action': 'browser.page.goto', 'args': ['https://google.com']}

action2 = context.page.goto("https://google.com")
print(action2.to_dict())  # {'action': 'page.goto', 'args': ['https://google.com']}

action1 = context.goto("https://google.com")
print(action1.to_dict())  # {'action': 'goto', 'args': ['https://google.com']}

print(list(map(lambda a: a.to_dict(), context.actions)))
