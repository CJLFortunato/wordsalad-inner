def get_progress_color(percentage: float):
  if percentage > 0 and percentage <= 33:
    return 'hsl(0, 50%, 60%)'

  if percentage > 33 and percentage < 100:
    return 'hsl(45, 95%, 70%)'

  if percentage >= 100 and percentage <= 110:
    return 'hsl(130, 70%, 70%)'

  if percentage > 110:
    return 'hsl(260, 50%, 70%)'

  return 'hsl(210, 10%, 40%)'