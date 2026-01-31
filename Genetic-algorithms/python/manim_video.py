from manim import *
import numpy as np


class RouletteWheelSelection(Scene):
    def construct(self):
        # --- CONFIGURACIÓN DE DATOS ---
        data = [
            {"label": "A", "fitness": 10, "color": RED_D},
            {"label": "B", "fitness": 25, "color": BLUE_D},
            {"label": "C", "fitness": 15, "color": GREEN_D},
            {"label": "D", "fitness": 40, "color": ORANGE},
            {"label": "E", "fitness": 10, "color": PURPLE_D},
        ]

        total_fitness = sum(d["fitness"] for d in data)
        curr_angle, curr_height = 0, 0
        wheel = VGroup()
        prob_bar_group = VGroup()
        bar_x_pos = 5

        # --- CONSTRUCCIÓN DE OBJETOS ---
        for d in data:
            prop = d["fitness"] / total_fitness
            angle = prop * TAU

            # Sector de la ruleta (Donut)
            sector = AnnularSector(
                inner_radius=0.8,
                outer_radius=2.5,
                angle=angle,
                start_angle=curr_angle,
                color=d["color"],
                fill_opacity=0.8,
                stroke_width=2,
                stroke_color=WHITE,
            )

            # Label radial dentro del sector
            mean_angle = curr_angle + angle / 2
            label = Text(d["label"], weight=BOLD).scale(0.7)
            label.move_to(np.array([np.cos(mean_angle), np.sin(mean_angle), 0]) * 1.7)

            unit = VGroup(sector, label)
            unit.label_name = d["label"]
            wheel.add(unit)

            # Barra lateral con porcentajes
            seg_h = prop * 5
            rect = Rectangle(
                width=0.8, height=seg_h, fill_color=d["color"], fill_opacity=0.8
            )
            rect.move_to([bar_x_pos, -2.5 + curr_height + seg_h / 2, 0])
            p_text = Text(f"{int(prop*100)}%", font_size=18).next_to(
                rect, RIGHT, buff=0.2
            )

            bar_segment = VGroup(rect, p_text)
            bar_segment.label_name = d["label"]
            prob_bar_group.add(bar_segment)

            curr_angle += angle
            curr_height += seg_h

        # Elementos estáticos
        pointer = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.2)
            .rotate(90 * DEGREES)
            .move_to(RIGHT * 2.8)
        )
        bar_outline = Rectangle(width=0.9, height=5.1, color=GRAY_A).move_to(
            [bar_x_pos, 0, 0]
        )
        title = Title("Selección de Ruleta (Algoritmos Genéticos)")

        # --- ANIMACIÓN INICIAL ---
        self.add(title)
        self.play(
            Create(wheel), FadeIn(prob_bar_group), Create(bar_outline), Create(pointer)
        )
        self.wait(1)

        # --- GIRO DE LA RULETA ---
        # Elegimos una rotación aleatoria entre 2 y 4 vueltas completas
        random_rot = np.random.uniform(TAU * 2, TAU * 4)
        self.play(
            Rotate(wheel, angle=random_rot, about_point=ORIGIN, rate_func=slow_into),
            run_time=4,
        )

        # --- LÓGICA PARA DETERMINAR EL GANADOR ---
        # El puntero está en el ángulo 0. Calculamos qué sector quedó ahí.
        winner_angle = (-random_rot) % TAU
        accum, winner_label, winner_color = 0, "?", WHITE

        for d in data:
            limit = accum + (d["fitness"] / total_fitness) * TAU
            if accum <= winner_angle <= limit:
                winner_label, winner_color = d["label"], d["color"]
                break
            accum = limit

        # --- MOSTRAR RESULTADO Y RESALTADO ---
        chosen_header = (
            Text("Elegido: ", font_size=28)
            .to_edge(DOWN, buff=1.2)
            .shift(LEFT * 0.8)
            .shift(DOWN * 0.2)
        )
        winner_display = Text(
            f"Individuo {winner_label}", color=winner_color, weight=BOLD
        ).scale(1.1)
        winner_display.next_to(chosen_header, RIGHT, buff=0.3)

        self.play(Write(chosen_header), FadeIn(winner_display, shift=UP))

        # Animaciones de resaltado simultáneas (Sectors, Barra y Texto)
        highlight_animations = [
            Indicate(winner_display, color=winner_color, scale_factor=1.3)
        ]

        for unit in wheel:
            if unit.label_name == winner_label:
                highlight_animations.append(unit.animate.scale(1.2).set_opacity(1))

        for bar in prob_bar_group:
            if bar.label_name == winner_label:
                highlight_animations.append(Indicate(bar[0], color=WHITE))

        self.play(*highlight_animations, run_time=1.5)
        self.wait(2)
