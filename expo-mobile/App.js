import React from 'react';
import { SafeAreaView, ActivityIndicator, View, StyleSheet } from 'react-native';
import { WebView } from 'react-native-webview';

const WEBAPP_URL = 'http://192.168.0.106:5000';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <WebView
        source={{ uri: WEBAPP_URL }}
        startInLoadingState
        renderLoading={() => (
          <View style={styles.loading}>
            <ActivityIndicator size="large" color="#2563eb" />
          </View>
        )}
        javaScriptEnabled
        domStorageEnabled
        allowsBackForwardNavigationGestures
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loading: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
});
