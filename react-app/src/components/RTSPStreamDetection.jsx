import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  Paper,
  Typography,
  Container,
  Alert,
  CircularProgress
} from '@mui/material';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import StopCircleIcon from '@mui/icons-material/StopCircle';

const RTSPStreamDetection = () => {
  const [rtspUrl, setRtspUrl] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const imageRef = useRef(null);

  const startStream = async () => {
    if (!rtspUrl) {
      setError('Vui lòng nhập URL RTSP');
      return;
    }

    try {
      setLoading(true);
      setError('');
      setIsStreaming(true);

      // Encode URL trước khi gửi request
      const encodedUrl = encodeURIComponent(rtspUrl);
      const streamUrl = `http://localhost:8000/api/stream-rtsp?rtsp_url=${encodedUrl}`;
      console.log('Encoded stream URL:', streamUrl);
      
      if (imageRef.current) {
        imageRef.current.src = streamUrl;
        
        imageRef.current.onerror = () => {
          setError('Mất kết nối stream. Đang thử kết nối lại...');
        };
      }

    } catch (err) {
      console.error('Stream error:', err);
      setError('Không thể kết nối đến stream: ' + err.message);
      setIsStreaming(false);
    } finally {
      setLoading(false);
    }
  };

  const stopStream = () => {
    if (imageRef.current) {
      imageRef.current.src = '';
    }
    setIsStreaming(false);
    setError('');
  };

  useEffect(() => {
    return () => {
      stopStream();
    };
  }, []);

  return (
    <Container maxWidth="lg">
      <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
        <Typography variant="h5" gutterBottom>
          Nhận diện biển báo qua RTSP Stream
        </Typography>

        <Box sx={{ mb: 3 }}>
          <TextField
            fullWidth
            label="RTSP URL"
            variant="outlined"
            value={rtspUrl}
            onChange={(e) => setRtspUrl(e.target.value)}
            placeholder="rtsp://camera-ip:port/stream"
            disabled={isStreaming}
            sx={{ mb: 2 }}
          />

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={startStream}
              disabled={isStreaming || loading}
              startIcon={<PlayCircleOutlineIcon />}
            >
              {loading ? <CircularProgress size={24} /> : 'Bắt đầu Stream'}
            </Button>

            <Button
              variant="contained"
              color="error"
              onClick={stopStream}
              disabled={!isStreaming}
              startIcon={<StopCircleIcon />}
            >
              Dừng Stream
            </Button>
          </Box>
        </Box>

        <Box
          sx={{
            width: '100%',
            height: '600px',
            bgcolor: 'black',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            overflow: 'hidden'
          }}
        >
          <img
            ref={imageRef}
            alt="RTSP Stream"
            style={{
              maxWidth: '100%',
              maxHeight: '100%',
              objectFit: 'contain'
            }}
          />
        </Box>
      </Paper>
    </Container>
  );
};

export default RTSPStreamDetection; 