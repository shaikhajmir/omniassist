import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { AlertCircle, Flame, Car, HeartPulse, Activity, Zap, ShieldAlert, CheckCircle } from 'lucide-react';
import axios from 'axios';

// Fix for leaflet icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const criticalIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const defaultIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});


const Dashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('Connecting...');

  useEffect(() => {
    // Fetch initial alerts
    axios.get('http://localhost:8000/alerts')
      .then(res => setAlerts(res.data.alerts || []))
      .catch(err => console.error("Could not fetch alerts:", err));

    // Connect WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => setConnectionStatus('Connected');
    ws.onclose = () => setConnectionStatus('Disconnected');
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'NEW_ALERT') {
        setAlerts(prev => [message.data, ...prev]);
      }
    };

    return () => ws.close();
  }, []);

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'CRITICAL': return 'bg-critical text-white pulse-critical';
      case 'HIGH': return 'bg-warning text-white';
      default: return 'bg-blue-500 text-white';
    }
  };

  const getIcon = (severity) => {
    switch(severity) {
      case 'CRITICAL': return <Flame className="w-5 h-5" />;
      case 'HIGH': return <AlertCircle className="w-5 h-5" />;
      default: return <Activity className="w-5 h-5" />;
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-100px)]">
      
      {/* Map Section */}
      <div className="lg:col-span-2 glass-panel rounded-xl overflow-hidden relative border border-gray-800 shadow-2xl">
        <div className="absolute top-4 left-4 z-[400] glass-panel px-4 py-2 rounded-lg pointer-events-none flex items-center space-x-2">
            <ShieldAlert className="text-accent w-5 h-5" />
            <span className="font-semibold text-sm tracking-wide shadow-black drop-shadow-md">LIVE INCIDENT MAP</span>
        </div>
        <MapContainer center={[37.7749, -122.4194]} zoom={13} style={{ height: '100%', width: '100%', background: '#0F172A' }}>
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://carto.com/">CartoDB</a>'
          />
          {alerts.map((alert, idx) => (
            alert.location && 
            <Marker 
              key={idx} 
              position={[alert.location.lat, alert.location.lng]}
              icon={alert.decision.severity === 'CRITICAL' ? criticalIcon : defaultIcon}
            >
              <Popup className="custom-popup">
                <div className="font-sans font-semibold text-gray-800">
                  <p className="text-red-600 mb-1">{alert.decision.severity} ALERT</p>
                  <p className="text-sm">{alert.decision.summary}</p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Alerts Feed */}
      <div className="glass-panel rounded-xl flex flex-col overflow-hidden border border-gray-800 shadow-2xl">
        <div className="p-4 border-b border-gray-800 bg-gray-900/50 flex justify-between items-center">
          <h2 className="text-xl font-bold flex items-center"><Zap className="mr-2 text-accent" /> Active Alerts</h2>
          <span className="text-xs bg-gray-800 px-2 py-1 rounded-full">{alerts.length} Total</span>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {alerts.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <CheckCircle className="w-12 h-12 mb-2 opacity-20" />
              <p>No active incidents</p>
            </div>
          ) : (
            alerts.map((alert, idx) => (
              <div key={idx} className="bg-gray-800/50 rounded-lg p-4 border border-gray-700 hover:border-gray-500 transition-colors duration-300">
                <div className="flex justify-between items-start mb-2">
                  <div className={`px-2 py-1 rounded text-xs font-bold flex items-center shadow-lg ${getSeverityColor(alert.decision.severity)}`}>
                    {getIcon(alert.decision.severity)}
                    <span className="ml-1">{alert.decision.severity}</span>
                  </div>
                  <span className="text-xs text-gray-400 font-mono">
                    {new Date(alert.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                
                <p className="text-sm font-medium mb-3">{alert.decision.summary}</p>
                
                <div className="grid grid-cols-3 gap-2 text-xs">
                    <div className="bg-gray-900/60 p-2 rounded border border-gray-800 flex flex-col items-center">
                        <span className="text-gray-500 mb-1">VISION</span>
                        <span className={alert.vision_data?.crisis ? 'text-red-400 font-bold' : 'text-green-400'}>
                            {alert.vision_data?.crisis ? 'DETECTED' : 'CLEAR'}
                        </span>
                    </div>
                    <div className="bg-gray-900/60 p-2 rounded border border-gray-800 flex flex-col items-center">
                        <span className="text-gray-500 mb-1">AUDIO</span>
                        <span className={alert.audio_data?.crisis ? 'text-red-400 font-bold' : 'text-green-400'}>
                            {alert.audio_data?.crisis ? 'DETECTED' : 'CLEAR'}
                        </span>
                    </div>
                    <div className="bg-gray-900/60 p-2 rounded border border-gray-800 flex flex-col items-center">
                        <span className="text-gray-500 mb-1">NLP</span>
                        <span className={alert.nlp_data?.crisis ? 'text-red-400 font-bold' : 'text-green-400'}>
                            {alert.nlp_data?.crisis ? 'DETECTED' : 'CLEAR'}
                        </span>
                    </div>
                </div>

                <div className="mt-3 flex justify-between items-center text-xs">
                    <span className="text-gray-500">Confidence: <span className="text-white font-bold">{alert.decision.confidence_score}%</span></span>
                    <button className="text-accent hover:text-white transition-colors">View Details &rarr;</button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

    </div>
  );
};

export default Dashboard;
