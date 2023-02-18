import typing

import dash_mantine_components as dmc


def icon_butt_img(img_url, id_: typing.Union[str, dict], class_name="action-icon", is_text=False, pad=4, style=None):
    return dmc.ActionIcon(
        dmc.Text(img_url) if is_text else dmc.Image(src=img_url), className=class_name, id=id_, p=pad, style=style if style else dict())


def button_with_icon(text, id_="", image_src="", class_name="custom_butt", size="md", disabled=False, color="orange", **style):
    extras = dict(style=dict(width="100%"), color=color, size=size)
    extras.update(id=id_, **style) if id_ else ...

    return dmc.Button(
        text, disabled=disabled, className=class_name, leftIcon=[dmc.Avatar(
            src=image_src, size="sm"
        )], **extras)