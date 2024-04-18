#Import statements appear at the beginning...
#Before any app coding occurs

import plotly.express as px
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
import palmerpenguins
from shinyswatch import theme


#Define dataframe (df) and load data
df = palmerpenguins.load_penguins()

#Using Page options, Customize Page Title
ui.page_opts(title="JGanyo Penguins dashboard", 
             fillable=True, 
            )
theme.yeti()

#Create Sidebar for user interactive choices
#Add Custom title to sidebar menu

with ui.sidebar(title="Filter Options"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
#Create horizontal rule for next set of 
#input including all links
    ui.hr()
#Name the side bar section 
    #since it is a 'new' topic=links
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

#Create the main body of the app
#using column wrap layout,
#Value box user interface cards for each unique
#characteristic (# of Penguins, Avg Bill Length, Avg Bill depth & scatterplot)

with ui.layout_column_wrap(fill=False):
#Is it trademark infrigement to use the Linux Penguin in this manner?
    with ui.value_box(showcase=icon_svg("linux")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():

    #build User Interface with Seaborn Scatterplot
    with ui.card(full_screen=True):        
        ui.card_header("Bill length vs depth")

        @render.plot(alt="A Seaborn scatterplot comparing bill length and depth in millimeters.")
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species"
                )
 
    #Build User Interface with Plotly Histogram
    with ui.card(full_screen=True):
        ui.card_header("Plotly Interactive")
        ui.input_selectize("var", "Select variable",
                           choices=["bill_length_mm", "body_mass_g"])
        @render_plotly
        def hist():
          return px.histogram(df, x=input.var())

    
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
