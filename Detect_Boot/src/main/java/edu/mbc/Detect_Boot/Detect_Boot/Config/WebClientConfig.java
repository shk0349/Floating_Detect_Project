package edu.mbc.Detect_Boot.Detect_Boot.Config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {

    @Bean
    WebClient webClient() {
        return WebClient.builder().exchangeStrategies(ExchangeStrategies.builder()
                .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(-1))    //... 무제한 버퍼
                .build())
                .baseUrl("http://localhost:5151")    //... Python AI 서버 주소 기재 / 업로드한 파일을 AI 서버에 전송하기 위하여 버퍼의 크기 제한을 없앰
                .build();
    }

} //... WebClient를 구성하고 Bean으로 정의하여 Application에서 사용할 수 있게함 / 참고 URL https://m.blog.naver.com/seek316/223337685249
