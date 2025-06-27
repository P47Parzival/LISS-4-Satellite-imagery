import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plus, MapPin, Calendar, Settings, Trash2, Eye, Search } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

interface AOI {
  _id: string;
  name: string;
  changeType: string;
  monitoringFrequency: string;
  status: string;
  createdAt: string;
  lastMonitored?: string;
  confidenceThreshold: number;
  description?: string;
}

export default function AOIList() {
  const [aois, setAois] = useState<AOI[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    fetchAOIs();
  }, []);

  const fetchAOIs = async () => {
    try {
      const response = await axios.get('http://localhost:8000/aois/');
      setAois(response.data);
    } catch (error) {
      console.error('Error fetching AOIs:', error);
      toast.error('Failed to fetch AOIs');
    } finally {
      setLoading(false);
    }
  };

  const deleteAOI = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this AOI?')) {
      return;
    }

    try {
      await axios.delete(`http://localhost:8000/aois/${id}`);
      setAois(aois.filter(aoi => aoi._id !== id));
      toast.success('AOI deleted successfully');
    } catch (error) {
      toast.error('Failed to delete AOI');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'inactive':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const filteredAOIs = aois.filter(aoi => {
    const matchesSearch = aoi.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         aoi.changeType.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || aoi.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="bg-white p-6 rounded-xl shadow-sm">
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My AOIs</h1>
          <p className="text-gray-600 mt-1">Manage your Areas of Interest</p>
        </div>
        <Link
          to="/create-aoi"
          className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
        >
          <Plus className="inline-block w-5 h-5 mr-2" />
          New AOI
        </Link>
      </div>

      {/* Filters */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search AOIs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="pending">Pending</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      {/* AOI Grid */}
      {filteredAOIs.length > 0 ? (
        <div className="grid gap-6">
          {filteredAOIs.map((aoi) => (
            <div key={aoi._id} className="bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200">
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-3">
                      <h3 className="text-xl font-semibold text-gray-900">{aoi.name}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(aoi.status)}`}>
                        {aoi.status}
                      </span>
                    </div>
                    
                    {aoi.description && (
                      <p className="text-gray-600 mb-4">{aoi.description}</p>
                    )}
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                      <div className="flex items-center text-gray-600">
                        <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                        <span className="capitalize">{aoi.changeType.replace(/([A-Z])/g, ' $1')}</span>
                      </div>
                      <div className="flex items-center text-gray-600">
                        <Calendar className="h-4 w-4 mr-2 text-gray-400" />
                        <span className="capitalize">{aoi.monitoringFrequency}</span>
                      </div>
                      <div className="flex items-center text-gray-600">
                        <Settings className="h-4 w-4 mr-2 text-gray-400" />
                        <span>{aoi.confidenceThreshold}% confidence</span>
                      </div>
                    </div>
                    
                    <div className="mt-4 flex items-center justify-between text-sm text-gray-500">
                      <span>Created: {formatDate(aoi.createdAt)}</span>
                      <span>
                        Last monitored: {aoi.lastMonitored ? formatDate(aoi.lastMonitored) : 'Never'}
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2 ml-6">
                    <button className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                      <Eye className="h-5 w-5" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                      <Settings className="h-5 w-5" />
                    </button>
                    <button 
                      onClick={() => deleteAOI(aoi._id)}
                      className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
          <MapPin className="mx-auto h-16 w-16 text-gray-400 mb-6" />
          <h3 className="text-xl font-medium text-gray-900 mb-2">
            {searchTerm || filterStatus !== 'all' ? 'No AOIs match your criteria' : 'No AOIs created yet'}
          </h3>
          <p className="text-gray-500 mb-8">
            {searchTerm || filterStatus !== 'all' 
              ? 'Try adjusting your search or filter criteria'
              : 'Create your first Area of Interest to start monitoring satellite data'
            }
          </p>
          <Link
            to="/create-aoi"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
          >
            <Plus className="mr-2 h-5 w-5" />
            Create your first AOI
          </Link>
        </div>
      )}
    </div>
  );
}