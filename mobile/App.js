import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// Screens
import LoginScreen from './screens/LoginScreen';
import CaseListScreen from './screens/CaseListScreen';
import DocumentViewerScreen from './screens/DocumentViewerScreen';
import SettingsScreen from './screens/SettingsScreen';

// Services
import PushNotificationService from './services/PushNotificationService';
import OfflineStorage from './services/OfflineStorage';
import ApiService from './services/ApiService';

const Stack = createStackNavigator();

const App = () => {
  React.useEffect(() => {
    // Initialize services
    PushNotificationService.configure();
    OfflineStorage.initialize();
    ApiService.configure();
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Cases" component={CaseListScreen} />
        <Stack.Screen name="DocumentViewer" component={DocumentViewerScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;