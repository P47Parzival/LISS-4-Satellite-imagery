// AOIAlertsModal.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Alert {
    _id: string;
    detection_date: string;
    area_of_change: number;
    before_image_url: string;
    after_image_url: string;
    status: string;
}

export default function AOIAlertsModal({ aoiId, onClose }: { aoiId: string, onClose: () => void }) {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get(`http://localhost:8000/aois/${aoiId}/changes`)
            .then(res => setAlerts(res.data))
            .catch(err => {
                if (err.response && err.response.status === 404) {
                    setAlerts([]);
                }
            })
            .finally(() => setLoading(false));
    }, [aoiId]);

    return (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-2xl relative">
                <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-700 text-xl">&times;</button>
                <h2 className="text-lg font-bold mb-4">Change Alerts</h2>
                {loading ? (
                    <div>Loading...</div>
                ) : alerts.length === 0 ? (
                    <div>No alerts for this AOI yet.</div>
                ) : (
                    <ul className="space-y-6">
                        {alerts.map(alert => (
                            <li key={alert._id} className="bg-gray-50 rounded-lg p-4">
                                <div className="mb-2 text-gray-700">
                                    <strong>Date:</strong> {new Date(alert.detection_date).toLocaleString()}
                                </div>
                                <div className="mb-2 text-gray-700">
                                    <strong>Area of Change:</strong> {alert.area_of_change.toFixed(2)} m²
                                </div>
                                <div className="flex gap-4">
                                    <div>
                                        <div className="text-xs text-gray-500 mb-1">Before</div>
                                        <img src={alert.before_image_url} alt="Before" className="w-40 rounded" />
                                    </div>
                                    <div>
                                        <div className="text-xs text-gray-500 mb-1">After</div>
                                        <img src={alert.after_image_url} alt="After" className="w-40 rounded" />
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}