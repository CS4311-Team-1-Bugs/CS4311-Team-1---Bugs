class state(object):
    def __init__(self):
        print("Processing current state:", str(self))

    def on_event(selfself, event):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class idle(state):
    def on_event(selfself, event):
        if event == "run configured":
            return configured
        return

class configured(state):
    def on_event(selfself, event):
        if event == "execute run received":
            return active
        return

class active(state):
    def on_event(selfself, event):
        if event == "pause run received":
            return inactive
        return

class inactive(state):
    def on_event(selfself, event):
        if event == "terminate run received":
            return terminate

        elif event == "execute run received":
            return active
        return

class terminate(state):
    def on_event(selfself, event):
        if event == "completed":
            return terminate


