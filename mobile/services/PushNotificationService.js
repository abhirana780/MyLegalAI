import { Platform } from 'react-native';
import PushNotification from 'react-native-push-notification';
import PushNotificationIOS from '@react-native-community/push-notification-ios';
import ApiService from './ApiService';
import OfflineStorage from './OfflineStorage';

class PushNotificationService {
  static configure() {
    PushNotification.configure({
      onRegister: async (token) => {
        try {
          const user = await OfflineStorage.getItem('user');
          if (user) {
            await ApiService.registerDeviceToken({
              userId: user.id,
              deviceToken: token.token,
              platform: Platform.OS
            });
          }
        } catch (error) {
          console.error('Failed to register device token:', error);
        }
      },
      onNotification: (notification) => {
        if (Platform.OS === 'ios') {
          notification.finish(PushNotificationIOS.FetchResult.NoData);
        }
        // Handle notification
        console.log('Notification received:', notification);
      },
      permissions: {
        alert: true,
        badge: true,
        sound: true,
      },
      popInitialNotification: true,
      requestPermissions: true,
    });
  }

  static scheduleLocalNotification(title, message, data = {}) {
    PushNotification.localNotification({
      title,
      message,
      data,
      playSound: true,
      soundName: 'default',
      importance: 'high',
      vibrate: true,
    });
  }
}

export default PushNotificationService;