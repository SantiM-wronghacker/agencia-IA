"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador copy facebook ads
TECNOLOGÍA: Python estándar
"""

import sys
import random
from datetime import datetime

def generate_copy(city=None, product=None, discount=None, date=None):
    products = ["Ropa deportiva", "Zapatos casuales", "Accesorios de moda", "Bolsas de diseño", "Relojes elegantes"]
    discounts = ["20%", "30%", "40%", "50%", "60%"]
    cities = ["CDMX", "Guadalajara", "Monterrey", "Puebla", "Querétaro"]
    dates = ["hoy", "mañana", "este fin de semana", "esta semana", "este mes"]

    if product is None:
        product = random.choice(products)
    if discount is None:
        discount = random.choice(discounts)
    if city is None:
        city = random.choice(cities)
    if date is None:
        date = random.choice(dates)

    copy = [
        f"¡OFERTA EXCLUSIVA EN {product.upper()}!",
        f"Solo {discount} de descuento en {product} en {city}.",
        f"¡Solo {date}! No te lo pierdas.",
        f"Envíos gratis a toda la República Mexicana.",
        f"¡Compra ahora y ahorra hasta $1,500 MXN!",
        f"Fecha de inicio: {datetime.now().strftime('%Y-%m-%d')}",
        f"Fecha de fin: {(datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')}",
        f"Precio original: $2,500 MXN",
        f"Precio con descuento: ${2500 - (2500 * int(discount.strip('%')) / 100)} MXN",
        f"Ahorrando: ${2500 - (2500 * int(discount.strip('%')) / 100)} MXN"
    ]

    return copy

def main():
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--help":
            print("Uso: python generador_copy_facebook_ads.py [ciudad] [producto] [descuento] [fecha]")
            return

        city = None
        product = None
        discount = None
        date = None

        if len(sys.argv) > 1:
            city = sys.argv[1]
        if len(sys.argv) > 2:
            product = sys.argv[2]
        if len(sys.argv) > 3:
            discount = sys.argv[3]
        if len(sys.argv) > 4:
            date = sys.argv[4]

        copy = generate_copy(city, product, discount, date)
        for line in copy:
            print(line)

        print("\nResumen Ejecutivo:")
        print("Se ha generado un copy para una oferta exclusiva en Facebook Ads.")
        print("La oferta incluye un descuento en un producto en una ciudad específica.")
        print("La fecha de inicio y fin de la oferta se han establecido automáticamente.")
        print("El precio original y el precio con descuento se han calculado automáticamente.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()