import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet-draw'
import './MapView.css'

// Fix for default marker icons in Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

function MapView({ onAOIChange }) {
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  const drawnItemsRef = useRef(null)
  const [areaSize, setAreaSize] = useState(null)

  useEffect(() => {
    if (!mapInstanceRef.current) {
      // Initialize map
      const map = L.map(mapRef.current).setView([20, 0], 2)
      
      // Add tile layer
      const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      })
      tileLayer.addTo(map)
      
      // Initialize FeatureGroup for drawn items
      const drawnItems = new L.FeatureGroup()
      map.addLayer(drawnItems)
      drawnItemsRef.current = drawnItems
      
      // Initialize draw control
      const drawControl = new L.Control.Draw({
        position: 'topright',
        draw: {
          polygon: {
            allowIntersection: false,
            shapeOptions: {
              color: '#3b82f6',
              fillOpacity: 0.2,
            }
          },
          rectangle: {
            shapeOptions: {
              color: '#3b82f6',
              fillOpacity: 0.2,
            }
          },
          circle: false,
          circlemarker: false,
          marker: false,
          polyline: false,
        },
        edit: {
          featureGroup: drawnItems,
          remove: true
        }
      })
      map.addControl(drawControl)
      
      // Handle draw events
      map.on(L.Draw.Event.CREATED, (e) => {
        drawnItems.clearLayers()
        const layer = e.layer
        drawnItems.addLayer(layer)
        
        const geoJSON = layer.toGeoJSON()
        const bounds = layer.getBounds()
        
        // Calculate area in km²
        const area = L.GeometryUtil ? 
          L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]) / 1000000 : 
          calculateArea(layer)
        
        setAreaSize(area.toFixed(2))
        
        onAOIChange({
          type: 'Feature',
          geometry: geoJSON.geometry,
          properties: {
            bounds: {
              north: bounds.getNorth(),
              south: bounds.getSouth(),
              east: bounds.getEast(),
              west: bounds.getWest(),
            }
          }
        })
      })
      
      map.on(L.Draw.Event.DELETED, () => {
        onAOIChange(null)
        setAreaSize(null)
      })
      
      map.on(L.Draw.Event.EDITED, (e) => {
        const layers = e.layers
        layers.eachLayer((layer) => {
          const geoJSON = layer.toGeoJSON()
          const bounds = layer.getBounds()
          const area = calculateArea(layer)
          
          setAreaSize(area.toFixed(2))
          
          onAOIChange({
            type: 'Feature',
            geometry: geoJSON.geometry,
            properties: {
              bounds: {
                north: bounds.getNorth(),
                south: bounds.getSouth(),
                east: bounds.getEast(),
                west: bounds.getWest(),
              }
            }
          })
        })
      })
      
      mapInstanceRef.current = map
    }
    
    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [onAOIChange])
  
  // Simple area calculation fallback
  const calculateArea = (layer) => {
    const bounds = layer.getBounds()
    const latDiff = bounds.getNorth() - bounds.getSouth()
    const lngDiff = bounds.getEast() - bounds.getWest()
    // Rough approximation: 111 km per degree
    return latDiff * lngDiff * 111 * 111
  }

  return (
    <div className="map-view">
      <div ref={mapRef} className="map" />
      {areaSize && (
        <div className="map-info">
          📏 Area: ~{areaSize} km²
        </div>
      )}
      <div className="map-instructions">
        <p>🗺️ Draw a rectangle or polygon on the map to select your area of interest</p>
      </div>
    </div>
  )
}

export default MapView


