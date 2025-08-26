
#Model	#Related To	#Relationship Type
Patient	GlucoseLog	One-to-Many
Patient	Medication	One-to-Many
GlucoseLog	Patient	Many-to-One (via FK)
Medication	Patient	Many-to-One (via FK)
