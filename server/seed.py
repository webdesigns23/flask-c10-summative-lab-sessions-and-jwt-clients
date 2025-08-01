#!/usr/bin/env python3
from app import app
from models import db, User, CellarRecord

with app.app_context():
	db.drop_all()
	db.create_all()

	# Delete Records
	print("Deleting All Records...")
	CellarRecord.query.delete()
	User.query.delete()
	db.session.commit()

	# Create users, unique username, pw hashed before stored!
	print("Creating Users...")
	u1 = User(username = "Luna") 
	u1.password_hash = "kitten123"

	u2 = User(username = "Pew")
	u2.password_hash = "cat456"
	
	u3 = User(username = "Grumpkins")
	u3.password_hash = "grumpy789"
	
	u4 = User(username = "Bear")
	u4.password_hash = "pw102030"

	db.session.add_all([u1,u2,u3,u4])
	db.session.commit()

	# Create cellar record info
	print("Creating Wine Cellar Records...")
	cr1 = CellarRecord(
		user_id = u1.id,
		wine = "La Cana",
		grape = "Navia Albarino",
		country = "Spain",
		vintage = 2018,
		quantity = 7,
		tasting_notes = "Light Body, Dry, Balanced, Peach, Green Apple, Minerals")
	
	cr2 = CellarRecord(
		user_id = u1.id,
		wine = "La Spinetta",
		grape = "Langhe Nebbiolo",
		country = "Italy",
		vintage = 2022,
		quantity = 5,
		tasting_notes = "Full Body, Dry, Tannic, Acidic, Red Fruit, Earthy")
	
	cr3 = CellarRecord(
		user_id = u2.id,
		wine = "Domaine William Fevre",
		grape = "Chablis",
		country = "France",
		vintage = 2021,
		quantity = 10,
		tasting_notes = "Medium Body, Dry, Acidic, Citrus, Minerals, Pear")
	
	cr4 = CellarRecord(
		user_id = u2.id,
		wine = "Royal Tokaji",
		grape = "Furmint",
		country = "Hungary",
		vintage = 2019,
		quantity = 6,
		tasting_notes = "Balanced, Dry, Acidic, Apricot, Citrus, Honey, Minerals")
	
	cr5 = CellarRecord(
		user_id = u3.id,
		wine = "Leth",
		grape = "Fruner Veltliner",
		country = "Austria",
		vintage = 2019,
		quantity = 12,
		tasting_notes = "Light, Dry, Acidic, Pear, Green Apple, Citrus, Minerals")
	
	cr6 = CellarRecord(
		user_id = u4.id,
		wine = "Dautel",
		grape = "Reisling",
		country = "Germany",
		vintage = 2022,
		quantity = 12,
		tasting_notes = "Medium Body, Dry, Acidic, Peach, Citrus, Minerals")
	
	db.session.add_all([cr1, cr2, cr3, cr4, cr5, cr6])
	db.session.commit()


	print("🍷🍇Database seeded successfully!")

