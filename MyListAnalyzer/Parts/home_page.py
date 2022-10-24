import typing
from dash import Input, Output, callback, dcc, html, clientside_callback, ClientsideFunction, State, \
    no_update, callback_context, ALL, MATCH, ctx, get_app, register_page
import dash_mantine_components as dmc
from MyListAnalyzer.utils import get_mapping, starry_bg
from MyListAnalyzer.Components.malCreds import MalCredsModal
from MyListAnalyzer.Components.layout import expanding_layout, expanding_scroll
from MyListAnalyzer.Components.buttons import icon_butt, image_button
from MyListAnalyzer.Components.ModalManager import get_modal, make_modal_alive, enter_to_click
from MyListAnalyzer.Components.notifications import provider
from MyListAnalyzer.mappings.enums import main_app, home_page, mal_creds_modal
from MyListAnalyzer.Components.collection import add_user


class HomePage:
    def __init__(self):
        super().__init__()
        self.mal_creds = MalCredsModal()

        self.mal_creds.init()
        self.add_routes()

    def inside_children(self, set_active):
        paper_height = 250

        tabs = dmc.Tabs(
            [
                dmc.Tab(dmc.Paper(
                    _, style={"height": f"{paper_height - 69}px", "background": "transparent"}, p="md"),
                    label=label) for _, label in
                ((self.login_things(), "Login"), (self.show_view(), "Open"))]
            , color="orange", class_name="home_card", active=set_active)

        return [
            *starry_bg(),
            dcc.Location(mal_creds_modal.location),
            dmc.Affix(
                tabs
                , position={"top": f"calc(50% - {paper_height // 2}px)", "left": "calc(50% - 150px)"},
                style={"width": "300px", "height": f"{paper_height}px"}
            ),
            provider(mal_creds_modal.notify, home_page.testNote),
            html.Div([self.mal_creds.inside], id="modals")
        ]

    def layout(self, tab):
        return dmc.LoadingOverlay(
            children=self.inside_children(tab),
            id="home", loaderProps=main_app.loadingProps)

    def login_things(self):
        return expanding_layout(
            dmc.Text(home_page.greet, size="xs"),
            icon_butt(
                "MyAnimeList", id_=mal_creds_modal.triggerId, image_src=mal_creds_modal.logo,
                size="sm"),
            spacing="xl", align="center", position="center"
        )

    def connect_callbacks(self):
        ...

    def show_view(self):
        return expanding_layout(
            *(
                dcc.Link(
                    expanding_layout(
                        dmc.Text(link_text, color="blue", underline=True),
                        dmc.Text(desc, size="xs", color="orange"), align="center", position="center"
                    ), className="single_card", href=href, title=desc, refresh=True
                ) for link_text, href, desc in home_page.apps
            ))

    def add_routes(self):
        app = get_app()

        app.server.add_url_rule(
            self.mal_creds.route,
            view_func=self.mal_creds.tokens_to_cookies_show_2
        )
