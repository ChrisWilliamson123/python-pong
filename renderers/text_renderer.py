class TextRenderer:
    @staticmethod
    def draw_multiline_text_centered(surface, text, font, color, center_pos, line_spacing=10):
        lines = text.splitlines()
        rendered_lines = [font.render(line, True, color) for line in lines]

        # Calculate total height of the block
        total_height = sum(line.get_height() for line in rendered_lines) + line_spacing * (len(lines) - 1)

        # Start drawing from top of block
        y_offset = center_pos[1] - total_height // 2

        for line_surface in rendered_lines:
            line_rect = line_surface.get_rect(center=(center_pos[0], y_offset + line_surface.get_height() // 2))
            surface.blit(line_surface, line_rect)
            y_offset += line_surface.get_height() + line_spacing
