import pygame
import math
import time
from data.weather_data_html_style import weather_data

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
BACKGROUND_COLOR = (245, 245, 255)
FPS = 60

# Color mapping function
def temp_to_color(temp):
    """Convert temperature to RGB color"""
    t = max(25, min(35, temp))
    ratio = (t - 25) / 10
    # Color mapping: low temperature = cyan/blue, high temperature = pure red
    r = int(60 + 195 * ratio)      # High temp: r=255
    g = int(220 - 220 * ratio)     # High temp: g=0
    b = int(240 - 240 * ratio)     # High temp: b=0
    return (r, g, b)

class WeatherVisualization:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hong Kong Weather Art Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.day_idx = 0
        self.last_switch = 0
        self.switch_interval = 90  # 90 frames = 1.5 seconds at 60fps
        self.frame_count = 0
        
    def get_visual_params(self, description):
        """Get visual parameters based on weather description"""
        desc_lower = description.lower()
        
        if 'thunderstorm' in desc_lower:
            return {'size': 10, 'amp': 1.5}
        elif 'showers' in desc_lower and 'cloudy' in desc_lower:
            return {'size': 8, 'amp': 1.25}
        elif 'showers' in desc_lower:
            return {'size': 7, 'amp': 1.15}
        elif 'cloudy' in desc_lower:
            return {'size': 6, 'amp': 1.05}
        elif 'mainly fine' in desc_lower:
            return {'size': 5, 'amp': 1.0}
        elif 'fine' in desc_lower:
            return {'size': 4, 'amp': 0.9}
        else:
            return {'size': 4, 'amp': 1.0}
    
    def draw_curved_line(self, start_pos, end_pos, color, ball_index, ball_count):
        """Draw a curved line between two points - exact HTML replica"""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Calculate midpoint - exactly like HTML
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Curve offset calculation - exactly like HTML
        curve_offset = 38 * math.sin(self.frame_count * 0.03 + ball_index * 0.7)
        ctrl_x = mid_x + curve_offset * math.cos((ball_index / ball_count) * math.pi * 2 + self.frame_count * 0.01)
        ctrl_y = mid_y + curve_offset * math.sin((ball_index / ball_count) * math.pi * 2 + self.frame_count * 0.01)
        
        # Draw quadratic bezier curve using multiple line segments
        points = []
        for t in range(0, 21):  # 21 points for smooth curve
            t_norm = t / 20.0
            # Quadratic bezier formula
            x = (1-t_norm)**2 * start_x + 2*(1-t_norm)*t_norm * ctrl_x + t_norm**2 * end_x
            y = (1-t_norm)**2 * start_y + 2*(1-t_norm)*t_norm * ctrl_y + t_norm**2 * end_y
            points.append((int(x), int(y)))
        
        if len(points) > 1:
            pygame.draw.lines(self.screen, color, False, points, 2)
    
    def draw_weather_art(self, day_data):
        """Draw the main weather visualization"""
        temp = (day_data['temp_min'] + day_data['temp_max']) / 2
        humidity = (day_data['humidity_min'] + day_data['humidity_max']) / 2
        wind = day_data['wind_speed']
        description = day_data['description']
        
        # Get visual parameters
        params = self.get_visual_params(description)
        size = params['size']
        amp = params['amp']
        
        count = int(30 + humidity)
        alpha = int(80 + humidity * 1.5)
        color = temp_to_color(temp)
        
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        speed = 1 + wind * 0.7
        
        # Store ball positions for line drawing
        ball_positions = []
        
        # Draw balls - exactly like HTML
        for i in range(count):
            angle = 2 * math.pi * i / count + self.frame_count * 0.004 * speed
            group_wave = math.sin(self.frame_count * 0.025 + math.floor(i/5)) * 24 * amp  # Group rhythmic movement
            individual_wave = math.sin(self.frame_count * 0.07 + i * 0.8) * 18 * amp  # Individual rhythmic movement
            base_radius = 120 + 60 * (i % 3) + 20 * wind
            vertical_wave = group_wave + individual_wave
            radius = base_radius + vertical_wave
            
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle) + vertical_wave * 0.7
            
            ball_positions.append((int(x), int(y)))
            
            # Draw ball with random size variation - exactly like HTML
            s = size + math.floor(2 * (self.frame_count + i) % 10 / 10 * 2)  # Simulate random
            ball_alpha = min(255, alpha + 80)  # Match HTML alpha + 80
            
            # Draw circle with proper alpha blending
            circle_color = (*color, ball_alpha)
            pygame.draw.circle(self.screen, color, (int(x), int(y)), s)
        
        # Draw curved lines from center to each ball - exactly like HTML
        for i, pos in enumerate(ball_positions):
            self.draw_curved_line((cx, cy), pos, color, i, len(ball_positions))
    
    def draw_info(self, day_data):
        """Draw weather information on the left side"""
        # Description - split long text into multiple lines
        description = day_data['description']
        max_width = 500  # Maximum width for text in pixels
        
        # Split long descriptions into multiple lines
        words = description.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            text_width = self.font.size(test_line)[0]
            
            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw description lines
        y_offset = 40
        for line in lines:
            desc_text = self.font.render(line, True, (51, 51, 51))
            self.screen.blit(desc_text, (40, y_offset))
            y_offset += 30  # Line spacing
        
        # Date
        date_y = y_offset + 10
        date_text = self.small_font.render(day_data['date'], True, (102, 102, 102))
        self.screen.blit(date_text, (40, date_y))
        
        # Weather data
        info_y = date_y + 40
        temp_text = self.small_font.render(f"Temp: {day_data['temp_min']}~{day_data['temp_max']}°C", True, (68, 68, 68))
        humidity_text = self.small_font.render(f"Humidity: {day_data['humidity_min']}~{day_data['humidity_max']}%", True, (68, 68, 68))
        wind_text = self.small_font.render(f"Wind: {day_data['wind_speed']} m/s", True, (68, 68, 68))
        
        self.screen.blit(temp_text, (40, info_y))
        self.screen.blit(humidity_text, (40, info_y + 25))
        self.screen.blit(wind_text, (40, info_y + 50))
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.day_idx = (self.day_idx + 1) % len(weather_data)
                        self.last_switch = self.frame_count
                    elif event.key == pygame.K_LEFT:
                        self.day_idx = (self.day_idx - 1) % len(weather_data)
                        self.last_switch = self.frame_count
            
            # Auto switch date - exactly like HTML (frame-based)
            if self.frame_count - self.last_switch > self.switch_interval:
                self.day_idx = (self.day_idx + 1) % len(weather_data)
                self.last_switch = self.frame_count
            
            # Clear screen
            self.screen.fill(BACKGROUND_COLOR)
            
            # Get current day data
            current_day = weather_data[self.day_idx]
            
            # Draw visualization
            self.draw_weather_art(current_day)
            self.draw_info(current_day)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            self.frame_count += 1
        
        pygame.quit()

if __name__ == "__main__":
    viz = WeatherVisualization()
    viz.run()