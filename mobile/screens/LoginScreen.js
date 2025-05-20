import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import ApiService from '../services/ApiService';
import OfflineStorage from '../services/OfflineStorage';

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    try {
      setIsLoading(true);
      const response = await ApiService.login(email, password);
      
      // Store user data and token for offline access
      await OfflineStorage.setItem('user', response.user);
      await OfflineStorage.setItem('token', response.token);
      
      // Navigate to appropriate screen based on user type
      if (response.user.role === 'lawyer') {
        navigation.navigate('Cases');
      } else {
        navigation.navigate('Cases');
      }
    } catch (error) {
      Alert.alert('Login Failed', error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>LegalDefendAI</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button
        title="Login"
        onPress={handleLogin}
        disabled={isLoading}
      />
      <Text style={styles.footerText}>
        Don't have an account? Contact support
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 30,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
  footerText: {
    marginTop: 20,
    textAlign: 'center',
    color: 'gray',
  },
});

export default LoginScreen;