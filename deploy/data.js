// Property data storage
const STORAGE_KEY = 'real_estate_properties';

// Initialize properties from localStorage or use default data
let properties = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [
    {
        id: 1,
        title: "Modern Apartment in Downtown",
        price: "$350,000",
        location: "New York, NY",
        bedrooms: 2,
        bathrooms: 2,
        area: "1200 sq ft",
        image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
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
        image: "https://images.unsplash.com/photo-1613977257365-aaae5a9817ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
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
        image: "https://images.unsplash.com/photo-1568605114967-8130f3a36994?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        description: "Charming family home in a quiet neighborhood. Features a large backyard and modern kitchen."
    }
];

// Save properties to localStorage
const saveProperties = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(properties));
};

// Property data management functions
const PropertyData = {
    getAll: () => [...properties],
    
    add: (property) => {
        properties.push(property);
        saveProperties();
        return property;
    },
    
    update: (property) => {
        const index = properties.findIndex(p => p.id === property.id);
        if (index !== -1) {
            properties[index] = property;
            saveProperties();
            return property;
        }
        return null;
    },
    
    delete: (id) => {
        const index = properties.findIndex(p => p.id === id);
        if (index !== -1) {
            properties.splice(index, 1);
            saveProperties();
            return true;
        }
        return false;
    },
    
    duplicate: (property) => {
        const duplicatedProperty = {
            ...property,
            id: Date.now(),
            title: `${property.title} (Copy)`
        };
        properties.push(duplicatedProperty);
        saveProperties();
        return duplicatedProperty;
    }
}; 