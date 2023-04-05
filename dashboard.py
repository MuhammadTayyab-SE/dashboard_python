
import sys
from htmltools import *
sys.path.append('../')
from seprate_stage import find_stage, find_all_stages
from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui
from my_dashboard.static.style import *
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

app_ui = ui.page_fluid(
    head_content(tags.style(circle)),
    ui.panel_title("The Dashboard"),
        
        # upper body code
        ui.row(
            ui.column(3, 
                    ui.div(
                        div(
                            ui.h2(ui.output_text("apt1"),class_="h5"),
                            ui.span(
                                    ui.output_text("percentage1"), 
                                    style="color:#BF0037; width:50%;",
                                    class_="fw-extrabold mb-1 h2"
                            ),
                        ),
                        
                        # circle div
                        ui.div(
                            ui.span(ui.output_text("percentage1_"), style="color:#BF0037 !important;"),
                            div(
                                div(class_="first50-bar"),
                                div(class_="value-bar",style="border-color:#BF0037 !important;"), 
                            class_="left-half-clipper"
                            ), 
                            class_  = "progress-circle p23", 
                    ),
                        
                    style="width=100%", class_="d-flex justify-content-center"),
            class_="card border-0 shadow mx-4"
            ),
            ui.column(3, 
                    ui.div(
                        div(
                            ui.h2(ui.output_text("apt2"),class_="h5"),
                            ui.span(
                                    ui.output_text("percentage2"), 
                                    style="color:#FF6544; width:50%;",
                                    class_="fw-extrabold mb-1 h2"
                            ),
                        ),
                        
                        # circle div
                        ui.div(
                            ui.span(ui.output_text("percentage2_"), class_="", style="color:#FF6544 !important;"),
                            div(
                                div(class_="first50-bar"),
                                div(class_="value-bar",style="border-color:#FF6544; !important;"), 
                            class_="left-half-clipper"
                            ), 
                            class_  = "progress-circle p20", 
                        ),
                        
                    style="width=100%", class_="d-flex justify-content-center"),
            class_="card border-0 shadow"),
            ui.column(3, 
                    ui.div(
                        div(
                            ui.h2(ui.output_text("apt3"),class_="h5"),
                            ui.span(
                                    ui.output_text("percentage3"), 
                                    style="color:#FFCF32; width:50%;",
                                    class_="fw-extrabold mb-1 h2"
                            ),
                        ),
                        
                        # circle div
                        ui.div(
                            ui.span(ui.output_text("percentage3_"), style="color:#FFCF32 !important;"),
                            div(
                                div(class_="first50-bar"),
                                div(class_="value-bar", style="border-color:#FFCF32 !important;" ), 
                            class_="left-half-clipper"
                            ), 
                            class_  = "progress-circle p17",
                        ),
                        
                    style="width=100%", class_="d-flex justify-content-center"),
            class_="card border-0 shadow mx-4"),
            
        class_="d-flex justify-content-center mt-5"),
    
        # lower body code
        div(
            # div1
            # div for defining rows
            div(
                #div for margin-top
                div(
                    # div card boards
                    div(
                        # div for wrapping the text
                        div(
                            div(
                                span("The current stage of the attack: ",class_="h5"),
                                span(ui.output_text("current_attack_stage", inline=True),style="color:#BF0037;",class_="h5"),
                                class_="pt-5 px-2"
                            ),
                            div( 
                                span("The next stage of the attack: ",class_="h5 pt-5"),
                                span(ui.output_text("next_attack_stage", inline=True),style="color: #FF6544; !important;",class_="h5"),
                                class_="pt-5 px-2"
                            ),
                        ),
                    class_="card border-0 shadow mt-4", style="height:200px;"
                    ),
                class_="mt-4"
                ),
            class_="col-sm-8 col-md-5 col-lg-5 col-xl-5 mx-1 pt-5"
            ),
            
            #  div 2 for chart display
            div(
                ui.output_plot("piechart"),
                class_="col-sm-8 col-md-4 col-lg-4 col-xl-4 pt-4"
            ),
        class_="row d-flex justify-content-center"
        ),
style=body)


def server(input, output, session):
    
    output_filename = "./Dataset/crossM.csv"
    stage_filename = "./Dataset/Stages.xlsx"
    database_filename = "./Dataset/APT TTP Represotory.xlsx"
    
    top_techniques, top_stage = find_stage(output_filename,stages_file=stage_filename,database_filename=database_filename)
    all_stages = find_all_stages(stage_filename)
    apts = list(top_techniques.keys())

    @output
    @render.text
    def apt1():
        return apts[0]
    
    @output
    @render.text
    def percentage1():
        return f"{top_techniques[apts[0]]} %"
    @output
    @render.text
    def percentage1_():
        return f"{top_techniques[apts[0]]} %"
    
    @output
    @render.text
    def apt2():
        return apts[1]
    
    @output
    @render.text
    def percentage2():
        return f"{top_techniques[apts[1]]} %"
    
    @output
    @render.text
    def percentage2_():
        return f"{top_techniques[apts[1]]} %"
    
    @output
    @render.text
    def apt3():
        return apts[2]
    
    @output
    @render.text
    def percentage3():
        return f"{top_techniques[apts[2]]} %"
    
    @output
    @render.text
    def percentage3_():
        return f"{top_techniques[apts[2]]} %"
    
    # @output
    @render.text
    def class_for_percentage1():
        classe = ""
        if top_techniques[apts[0]] > 50:
            classe += "over50 "
        classe += f"p{top_techniques[apts[0]]}"
        return classe
    
    @output
    @render.text
    def class_for_percentage2():
        classe = ""
        if top_techniques[apts[1]] > 50:
            classe += "over50 "
        classe += f"p{top_techniques[apts[1]]}"
        return classe
    
    @output
    @render.text
    def class_for_percentage3():
        classe = ""
        if top_techniques[apts[2]] > 50:
            classe += "over50 "
        classe += f"p{top_techniques[apts[2]]}"
        return classe
    
    @output
    @render.text
    def current_attack_stage():
        return top_stage
    
    @output
    @render.text
    def next_attack_stage():
        index = all_stages.index(top_stage)
        if index < len(all_stages) - 1:
            return all_stages[index + 1]
        return "No next stage available"

    @output
    @render.plot
    def piechart():
        labels = list(top_techniques.keys())
        data = list(top_techniques.values())
        colors = ['#BF0037','#FF6544','#FFCF32']

        # fig = plt.pie(x=data, labels=labels, autopct='%1.1f%%', explode = [0.2, 0, 0],  startangle=0, l)
        # fig  =       plt.legend('', frameon=False)
        fig, ax = plt.subplots()
        patches, texts, autotexts = ax.pie(data, colors = colors, labels=labels, autopct='%1.0f%%', normalize=True,explode = [0.2, 0, 0], startangle=0)
        
        for text in autotexts:
            text.set_visible(False)
        return fig
        
app = App(app_ui, server, debug=True)
