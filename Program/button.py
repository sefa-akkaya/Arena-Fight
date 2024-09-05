class Button(): 
	def __init__(self, image, image_click,pos):
		self.image = self.defauilt_image = image     
		self.image_click = image_click   
		self.x_pos = pos[0]     
		self.y_pos = pos[1]   
		# self.text = self.font.render(self.text_input, True, self.base_color)   
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))       
           
	def update(self, screen):       
		if self.image is not None:    
			screen.blit(self.image, self.rect) 
  
	def checkForInput(self, position, is_wide):  
		if is_wide: 
			x_change = 70
			y_change = 60
		else:
			x_change = 0
			y_change = 0
		if position[0] in range(self.rect.left + x_change, self.rect.right -x_change) and position[1] in range(self.rect.top+y_change, self.rect.bottom-y_change):
			self.image = self.image_click
			return True
		return False

	def changeColor(self, position, is_wide):
		if is_wide:
			x_change = 70
			y_change = 60
		else:
			x_change = 0
			y_change = 0
		if position[0] in range(self.rect.left + x_change, self.rect.right -x_change) and position[1] in range(self.rect.top+y_change, self.rect.bottom-y_change):
			self.image = self.image_click
			return True
		else:
			self.image = self.defauilt_image
			return False
