import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

export default function MapView() {
  return (
    <MapContainer
      center={[11.0168, 76.9558]}
      zoom={13}
      style={{
        height: "400px",
        width: "100%",
        borderRadius: "12px",
        marginTop: "20px",
      }}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker position={[11.0168, 76.9558]}>
        <Popup>
          Recommended Hospital
        </Popup>
      </Marker>
    </MapContainer>
  );
}