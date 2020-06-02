from widark import Widget, Frame, Listbox, Label, Entry, Event, Modal, Color


class UsersScreen(Frame):
    class UserItem(Widget):
        def setup(self, **context) -> 'UserItem':
            self.item = context.pop('item', {})
            return super().setup(**context) and self

        def build(self) -> None:
            for i, field in enumerate(['id', 'name', 'email']):
                Label(self, content=f"{self.item.get(field)}").style(
                    Color.SUCCESS()).grid(0, i)

    def setup(self, **context) -> 'UsersScreen':
        self.authark_informer = context['injector']['AutharkInformer']
        return super().setup(**context) and self

    def build(self) -> None:
        self.modal = None
        Label(self, content='\U0001F50D Search:'
              ).grid(0, 0)
        self.search = Entry(self).grid(0, 1).style(border=[0])
        self.header = Listbox(
            self, data=['ID', 'Name', 'Email'],
            orientation='horizontal').grid(1).span(col=3)
        self.body = Listbox(
            self, command=self.on_body).grid(3).span(col=2).weight(11)
        self.listen('click', self.on_backdrop_click, True)

    async def load(self) -> None:
        users = (await self.authark_informer.search('user')) * 3
        self.body.setup(
            data=users, template=UsersScreen.UserItem).connect()

    async def on_body(self, event: Event) -> None:
        item = event.target.parent.item
        self.modal = UserDetailsModal(
            self, item=item, done_command=self.on_modal_done,
            proportion={'height': 0.90, 'width': 0.90}).launch()

    async def on_modal_done(self, event: Event) -> None:
        if self.modal:
            self.remove(self.modal)
            self.modal = None
            self.render()

    async def on_backdrop_click(self, event: Event) -> None:
        if self.modal and not self.modal.hit(event):
            event.stop = True
            self.remove(self.modal)
            self.modal = None
            self.render()


class UserDetailsModal(Modal):
    def setup(self, **context) -> 'UserDetailsModal':
        # self.authark_informer = context['injector']['AutharkInformer']
        self.item = context['item']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        Label(self, content=str(self.item))
