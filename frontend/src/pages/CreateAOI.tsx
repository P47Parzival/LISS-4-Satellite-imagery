import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import { Save, X } from 'lucide-react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import axios from 'axios';
import toast from 'react-hot-toast';

// Fix for default markers
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

interface AOIFormData {
  name: string;
  monitoringFrequency: string;
  changeType: string;
  confidenceThreshold: number;
  emailAlerts: boolean;
  inAppNotifications: boolean;
  description: string;
}

export default function CreateAOI() {
  const navigate = useNavigate();
  const mapRef = useRef<L.Map | null>(null);
  const [drawnShape, setDrawnShape] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState<AOIFormData>({
    name: '',
    monitoringFrequency: 'weekly',
    changeType: 'deforestation',
    confidenceThreshold: 60,
    emailAlerts: true,
    inAppNotifications: true,
    description: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({
        ...prev,
        [name]: checked
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const onCreated = (e: any) => {
    const { layer } = e;
    setDrawnShape(layer.toGeoJSON());
  };

  const onEdited = (e: any) => {
    const layers = e.layers;
    layers.eachLayer((layer: any) => {
      setDrawnShape(layer.toGeoJSON());
    });
  };

  const onDeleted = (e: any) => {
    setDrawnShape(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!drawnShape) {
      toast.error('Please draw an area on the map');
      return;
    }

    if (!formData.name.trim()) {
      toast.error('Please enter an AOI name');
      return;
    }

    setLoading(true);
    try {
      const aoiData = {
        name: formData.name,
        geojson: drawnShape,
        changeType: formData.changeType,
        monitoringFrequency: formData.monitoringFrequency,
        confidenceThreshold: formData.confidenceThreshold,
        emailAlerts: formData.emailAlerts,
        inAppNotifications: formData.inAppNotifications,
        description: formData.description,
        status: 'active'
      };

      await axios.post('http://localhost:8000/aois/', aoiData);
      toast.success('AOI created successfully!');
      navigate('/aois');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create AOI');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="max-w-7xl mx-auto">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Create New AOI</h1>
                <p className="text-gray-600 mt-1">Define an area of interest for satellite monitoring</p>
              </div>
              <button
                onClick={() => navigate('/aois')}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="h-6 w-6" />
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-6">
            {/* Map Section */}
            <div className="space-y-4">
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-2">Draw Your Area of Interest</h2>
                <p className="text-sm text-gray-600 mb-4">
                  Use the drawing tools to define the area you want to monitor. You can draw polygons or rectangles.
                </p>
              </div>

              <div className="h-96 rounded-lg overflow-hidden border border-gray-200">
                <MapContainer
                  center={[20.5937, 78.9629]} // Center of India
                  zoom={5}
                  style={{ height: '100%', width: '100%' }}
                  ref={mapRef}
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  />
                  <FeatureGroup>
                    <EditControl
                      position="topright"
                      onCreated={onCreated}
                      onEdited={onEdited}
                      onDeleted={onDeleted}
                      draw={{
                        polyline: true,
                        polygon: true,
                        rectangle: true,
                        circle: false,
                        circlemarker: false,
                        marker: true,
                      }}
                      edit={{
                        remove: true,
                      }}
                    />
                  </FeatureGroup>
                </MapContainer>
              </div>

              {drawnShape && (
                <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-sm text-green-800">
                    ✓ Area drawn successfully. You can edit or delete it using the map controls.
                  </p>
                </div>
              )}
            </div>

            {/* Form Section */}
            <div className="space-y-6">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    AOI Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., My Farmland in Gujarat"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Monitoring Frequency
                  </label>
                  <select
                    name="monitoringFrequency"
                    value={formData.monitoringFrequency}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="biweekly">Bi-Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Change Type (Primary Interest)
                  </label>
                  <select
                    name="changeType"
                    value={formData.changeType}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="deforestation">Deforestation / Vegetation Loss</option>
                    <option value="construction">Construction / Urbanization</option>
                    <option value="waterbody">Waterbody Changes</option>
                    <option value="agricultural">Agricultural Changes</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Confidence Threshold: {formData.confidenceThreshold}%
                  </label>
                  <input
                    type="range"
                    name="confidenceThreshold"
                    min="30"
                    max="90"
                    step="10"
                    value={formData.confidenceThreshold}
                    onChange={handleInputChange}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>Sensitive (30%)</span>
                    <span>Moderate (60%)</span>
                    <span>Strict (90%)</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    Notification Preferences
                  </label>
                  <div className="space-y-3">
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        name="emailAlerts"
                        checked={formData.emailAlerts}
                        onChange={handleInputChange}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-3 text-sm text-gray-700">Email Alerts</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        name="inAppNotifications"
                        checked={formData.inAppNotifications}
                        onChange={handleInputChange}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-3 text-sm text-gray-700">In-App Notifications</span>
                    </label>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description (Optional)
                  </label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Additional details about this AOI..."
                  />
                </div>

                <div className="flex space-x-4 pt-4">
                  <button
                    type="submit"
                    disabled={loading || !drawnShape}
                    className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                  >
                    {loading ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Creating...
                      </div>
                    ) : (
                      <div className="flex items-center justify-center">
                        <Save className="mr-2 h-5 w-5" />
                        Save AOI
                      </div>
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={() => navigate('/aois')}
                    className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}