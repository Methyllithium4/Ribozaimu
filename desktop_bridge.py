from dbus_next.service import ServiceInterface, method, signal
from dbus_next.aio import MessageBus
import asyncio
import threading


class DesktopBridgeInterface(ServiceInterface):

    def __init__(self, callback):
        super().__init__('org.zaimu.Desktop')
        self.callback = callback

    # KWin will call this
    @method()
    def WindowEvent(self, event_type: 's', app: 's', title: 's'):
        self.callback({
            "type": event_type,
            "app": app,
            "title": title
        })


class DesktopBridge:

    def __init__(self, callback):
        self.callback = callback
        self.loop = asyncio.new_event_loop()

    async def _run(self):
        bus = await MessageBus().connect()

        interface = DesktopBridgeInterface(self.callback)

        bus.export('/desktop', interface)

        await bus.request_name('org.zaimu.Desktop')

        await asyncio.Future()  # run forever

    def start(self):
        def runner():
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self._run())

        threading.Thread(target=runner, daemon=True).start()