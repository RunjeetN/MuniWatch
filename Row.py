class Row:
    def __init__(self, parent):
        self.container = parent.container()

    def render(self, data):
        img, a, b, c = self.container.columns([1, 2, 2, 2])

        with img:
            st.image(data.image)

        with a:
            st.write(data.a)

        with b:
            st.write(data.b)

        with c:
            st.write(data.c)