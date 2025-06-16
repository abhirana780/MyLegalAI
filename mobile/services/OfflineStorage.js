import AsyncStorage from '@react-native-async-storage/async-storage';

class OfflineStorage {
  static async initialize() {
    // Initialize any required storage configurations
  }

  static async setItem(key, value) {
    try {
      const jsonValue = JSON.stringify(value);
      await AsyncStorage.setItem(key, jsonValue);
    } catch (e) {
      console.error('Failed to save data to storage:', e);
    }
  }

  static async getItem(key) {
    try {
      const jsonValue = await AsyncStorage.getItem(key);
      return jsonValue != null ? JSON.parse(jsonValue) : null;
    } catch (e) {
      console.error('Failed to read data from storage:', e);
      return null;
    }
  }

  static async removeItem(key) {
    try {
      await AsyncStorage.removeItem(key);
    } catch (e) {
      console.error('Failed to remove data from storage:', e);
    }
  }

  static async clear() {
    try {
      await AsyncStorage.clear();
    } catch (e) {
      console.error('Failed to clear storage:', e);
    }
  }

  static async cacheDocument(documentId, documentData) {
    try {
      const documents = await this.getItem('cachedDocuments') || {};
      documents[documentId] = documentData;
      await this.setItem('cachedDocuments', documents);
    } catch (e) {
      console.error('Failed to cache document:', e);
    }
  }

  static async getCachedDocument(documentId) {
    try {
      const documents = await this.getItem('cachedDocuments') || {};
      return documents[documentId] || null;
    } catch (e) {
      console.error('Failed to get cached document:', e);
      return null;
    }
  }

  static async removeCachedDocument(documentId) {
    try {
      const documents = await this.getItem('cachedDocuments') || {};
      delete documents[documentId];
      await this.setItem('cachedDocuments', documents);
    } catch (e) {
      console.error('Failed to remove cached document:', e);
    }
  }
}

export default OfflineStorage;