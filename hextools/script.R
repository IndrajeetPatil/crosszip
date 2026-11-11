library(hexSticker)
library(magick)
library(showtext)

google_font_name <- "Rubik"
font_add_google(google_font_name)

showtext_auto()

img <- image_read("hextools/data.png")

logo_file <- "docs/assets/logo.png"

logo <- sticker(
    img,
    package = "crosszip",
    p_color = "#545452",
    p_family = google_font_name,
    p_size = 40,
    p_x = 1,
    p_y = 1.55,
    s_x = 1,
    s_y = 0.9,
    s_width = 1,
    s_height = 0.9,
    h_color = "grey",
    filename = logo_file,
    h_fill = "white",
    dpi = 600
)

# sticker() left-aligns the URL from u_x/u_y, so a short URL ends up bunched
# towards the bottom vertex. Draw it centred on the lower-right edge instead,
# inset from the border by the same distance as hexSticker's default.
edge_angle <- pi / 6
inset <- 0.08 * cos(edge_angle)
logo <- logo +
    geom_url(
        "indrapatil.com/crosszip",
        x = 1 + sqrt(3) / 4 - inset * sin(edge_angle),
        y = 0.25 + inset * cos(edge_angle),
        size = 8,
        color = "grey",
        hjust = 0.5
    )
save_sticker(logo_file, logo, dpi = 600)
