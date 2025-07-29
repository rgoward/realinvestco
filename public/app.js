// Sample property data
const properties = [
    {
        id: 1,
        title: "Modern Apartment in Downtown",
        price: "$350,000",
        location: "New York, NY",
        bedrooms: 2,
        bathrooms: 2,
        area: "1200 sq ft",
        image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267"
    },
    {
        id: 2,
        title: "Luxury Villa with Pool",
        price: "$1,200,000",
        location: "Los Angeles, CA",
        bedrooms: 4,
        bathrooms: 3,
        area: "3000 sq ft",
        image: "https://images.unsplash.com/photo-1613977257365-aaae5a9817ff"
    }
];

// Property Card Component
function PropertyCard({ property }) {
    return (
        <div className="property-card">
            <img src={property.image} alt={property.title} />
            <div className="property-info">
                <h3>{property.title}</h3>
                <p className="price">{property.price}</p>
                <p className="location">{property.location}</p>
                <div className="property-details">
                    <span>{property.bedrooms} beds</span>
                    <span>{property.bathrooms} baths</span>
                    <span>{property.area}</span>
                </div>
            </div>
        </div>
    );
}

// Search Component
function SearchBar() {
    return (
        <div className="search-bar">
            <input type="text" placeholder="Search by location..." />
            <select>
                <option value="">Price Range</option>
                <option value="0-300000">$0 - $300,000</option>
                <option value="300000-600000">$300,000 - $600,000</option>
                <option value="600000+">$600,000+</option>
            </select>
            <button>Search</button>
        </div>
    );
}

// Main App Component
function App() {
    return (
        <div className="app">
            <header>
                <h1>Real InvestCo</h1>
                <SearchBar />
            </header>
            <main>
                <div className="properties-grid">
                    {properties.map(property => (
                        <PropertyCard key={property.id} property={property} />
                    ))}
                </div>
            </main>
            <footer>
                <p>&copy; 2024 Real Estate Properties. All rights reserved.</p>
            </footer>
        </div>
    );
}

// Render the app
ReactDOM.render(<App />, document.getElementById('root')); 