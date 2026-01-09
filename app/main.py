from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.restaurant import router as restaurant_router



app = FastAPI(title="Food Ordering Backend")

# Include auth router
app.include_router(auth_router)
app.include_router(restaurant_router)



# @app.get("/")
# def root():
#     return {"message": "Backend is running"}



from app.routes.food import router as food_router
app.include_router(food_router)


from app.routes.order import router as order_router
app.include_router(order_router)



from app.routes.user import router as user_router
app.include_router(user_router)