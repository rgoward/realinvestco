// Property data storage
class PropertyData {
    static STORAGE_KEY = 'realInvestCo_properties';

    static getAll() {
        const data = localStorage.getItem(this.STORAGE_KEY);
        if (!data) {
            // Initialize with default data if none exists
            const defaultData = [
                {
                    id: 1,
                    title: "Modern Apartment in Downtown",
                    price: "$350,000",
                    location: "New York, NY",
                    bedrooms: 2,
                    bathrooms: 2,
                    area: "1200 sq ft",
                    images: [
                        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                    ],
                    description: "Beautiful modern apartment in the heart of downtown. Features floor-to-ceiling windows and a spacious balcony."
                },
                {
                    id: 2,
                    title: "Luxury Villa with Pool",
                    price: "$1,200,000",
                    location: "Los Angeles, CA",
                    bedrooms: 4,
                    bathrooms: 3,
                    area: "3000 sq ft",
                    images: [
                        "https://images.unsplash.com/photo-1613977257365-aaae5a9817ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1613977257365-aaae5a9817ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1613977257365-aaae5a9817ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                    ],
                    description: "Stunning luxury villa with private pool and garden. Perfect for entertaining and family living."
                },
                {
                    id: 3,
                    title: "Cozy Family Home",
                    price: "$450,000",
                    location: "Chicago, IL",
                    bedrooms: 3,
                    bathrooms: 2,
                    area: "1800 sq ft",
                    images: [
                        "https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                    ],
                    description: "Charming family home in a quiet neighborhood. Features a large backyard and modern kitchen."
                },
                {
                    id: 4,
                    title: "Waterfront Condo",
                    price: "$750,000",
                    location: "Miami, FL",
                    bedrooms: 3,
                    bathrooms: 2,
                    area: "2000 sq ft",
                    images: [
                        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                    ],
                    description: "Luxurious waterfront condo with stunning ocean views. Features modern amenities and private beach access."
                },
                {
                    id: 5,
                    title: "Mountain View Estate",
                    price: "$2,500,000",
                    location: "Denver, CO",
                    bedrooms: 5,
                    bathrooms: 4,
                    area: "4500 sq ft",
                    images: [
                        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                    ],
                    description: "Magnificent estate with panoramic mountain views. Features high-end finishes and extensive outdoor living spaces."
                }
            ];
            this.updateAll(defaultData);
            return defaultData;
        }
        return JSON.parse(data);
    }

    static getById(id) {
        const properties = this.getAll();
        return properties.find(p => p.id === parseInt(id));
    }

    static updateAll(properties) {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(properties));
        // Dispatch a custom event to notify other pages
        window.dispatchEvent(new CustomEvent('propertiesUpdated'));
    }

    static add(property) {
        const properties = this.getAll();
        property.id = Date.now();
        properties.push(property);
        this.updateAll(properties);
        return property;
    }

    static update(property) {
        const properties = this.getAll();
        const index = properties.findIndex(p => p.id === parseInt(property.id));
        if (index !== -1) {
            properties[index] = property;
            this.updateAll(properties);
            return true;
        }
        return false;
    }

    static delete(id) {
        const properties = this.getAll();
        const filtered = properties.filter(p => p.id !== parseInt(id));
        this.updateAll(filtered);
    }

    static duplicate(property) {
        const properties = this.getAll();
        const duplicatedProperty = {
            ...property,
            id: Date.now(),
            title: `${property.title} (Copy)`
        };
        properties.push(duplicatedProperty);
        this.updateAll(properties);
        return duplicatedProperty;
    }
}