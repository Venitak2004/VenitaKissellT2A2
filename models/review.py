from init import db
from datetime import date

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=date.today) #default to todays date
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
       
    user = db.relationship('User', back_populates='reviews')  
    products = db.relationship('Product', back_populates='reviews')
   

    def __repr__(self):
        return f'<Review {self.id}>'