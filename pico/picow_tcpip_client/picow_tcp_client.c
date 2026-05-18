/**
 * Pico 2 W - TCP Client: Random Data Sender & LED Controller
 */

 #include <string.h>
 #include <stdlib.h>
 #include <time.h>
 #include "pico/stdlib.h"
 #include "pico/cyw43_arch.h"
 #include "lwip/pbuf.h"
 #include "lwip/tcp.h"
 
 #define TCP_PORT 8000
 #define BUF_SIZE 2048
 
 typedef struct TCP_CLIENT_T_ {
     struct tcp_pcb *tcp_pcb;
     ip_addr_t remote_addr;
     bool complete;
     int run_count;
 } TCP_CLIENT_T;
 
 // 랜덤 온도 값 생성 (20.0 ~ 40.0)
 float get_random_value() {
     return 20.0f + (float)rand() / (float)(RAND_MAX / 20.0f);
 }
 
 // 서버로 데이터 전송 함수
 static err_t send_sensor_data(struct tcp_pcb *tpcb) {
     char buf[32];
     float val = get_random_value();
     int len = snprintf(buf, sizeof(buf), "%.2f", val);
     printf("Sending to server: %s\n", buf);
     return tcp_write(tpcb, buf, len, TCP_WRITE_FLAG_COPY);
 }
 
 static err_t tcp_client_close(void *arg) {
     TCP_CLIENT_T *state = (TCP_CLIENT_T*)arg;
     if (state->tcp_pcb != NULL) {
         tcp_arg(state->tcp_pcb, NULL);
         tcp_close(state->tcp_pcb);
         state->tcp_pcb = NULL;
     }
     state->complete = true;
     return ERR_OK;
 }
 
 // 서버로부터 LED 제어 명령 수신 시 호출
 err_t tcp_client_recv(void *arg, struct tcp_pcb *tpcb, struct pbuf *p, err_t err) {
     TCP_CLIENT_T *state = (TCP_CLIENT_T*)arg;
     if (!p) return tcp_client_close(arg);
 
     char rx_buf[32] = {0};
     pbuf_copy_partial(p, rx_buf, p->tot_len < 31 ? p->tot_len : 31, 0);
     printf("Server Command: %s\n", rx_buf);
 
     // LED 제어 로직
     if (strstr(rx_buf, "LED_ON")) {
         cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
     } else if (strstr(rx_buf, "LED_OFF")) {
         cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
     }
 
     tcp_recved(tpcb, p->tot_len);
     pbuf_free(p);
 
     // 1초 후 다음 데이터 전송 (반복 테스트용)
     sleep_ms(1000);
     state->run_count++;
     if (state->run_count < 20) { // 20회 테스트 후 종료
         send_sensor_data(tpcb);
     } else {
         tcp_client_close(arg);
     }
 
     return ERR_OK;
 }
 
 static err_t tcp_client_connected(void *arg, struct tcp_pcb *tpcb, err_t err) {
     if (err != ERR_OK) return tcp_client_close(arg);
     printf("Connected to server. Starting data transmission...\n");
     return send_sensor_data(tpcb); // 첫 번째 데이터 전송 시작
 }
 
 static void tcp_client_err(void *arg, err_t err) {
     printf("TCP Error: %d\n", err);
 }
 
 static bool tcp_client_open(void *arg) {
     TCP_CLIENT_T *state = (TCP_CLIENT_T*)arg;
     state->tcp_pcb = tcp_new_ip_type(IPADDR_TYPE_V4);
     if (!state->tcp_pcb) return false;
 
     tcp_arg(state->tcp_pcb, state);
     tcp_recv(state->tcp_pcb, tcp_client_recv);
     tcp_err(state->tcp_pcb, tcp_client_err);
 
     cyw43_arch_lwip_begin();
     err_t err_conn = tcp_connect(state->tcp_pcb, &state->remote_addr, TCP_PORT, tcp_client_connected);
     cyw43_arch_lwip_end();
 
     return err_conn == ERR_OK;
 }
 
 void run_tcp_client_test() {
     srand(time(NULL)); // 랜덤 시드 초기화
     TCP_CLIENT_T *state = calloc(1, sizeof(TCP_CLIENT_T));
     if (!state) return;
 
     ip4addr_aton(TEST_TCP_SERVER_IP, &state->remote_addr);
     
     if (tcp_client_open(state)) {
         while(!state->complete) {
             cyw43_arch_poll();
             sleep_ms(1);
         }
     }
     free(state);
 }
 
 int main() {
     stdio_init_all();
     if (cyw43_arch_init()) return 1;
     cyw43_arch_enable_sta_mode();
 
     printf("Connecting to Wi-Fi...\n");
     if (cyw43_arch_wifi_connect_timeout_ms(WIFI_SSID, WIFI_PASSWORD, CYW43_AUTH_WPA2_AES_PSK, 30000)) {
         printf("Wi-Fi connection failed.\n");
         return 1;
     }
     
     run_tcp_client_test();
     cyw43_arch_deinit();
     return 0;
 }