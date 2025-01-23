package edu.mbc.Detect_Boot.Detect_Boot.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@RestController    //... Python과 통신하는 비동기화 Controller 역할담당
public class RestRegController {

    @Autowired    //... 생성자 자동주입(객체사용)
    private WebClient webClient;    //... config 컨트롤러 객체 생성

    @PostMapping("/java_service")   //... Post 방식 처리용 Controller
    public String ServiceRequest(MultipartFile file, String message) {

        MultipartBodyBuilder bodyBuilder = new MultipartBodyBuilder();    //... Multipart Form Data 구성
        bodyBuilder.part("message", message);    //... Form Data
        bodyBuilder.part("file", file.getResource());    //... Form Data, File
        String result = webClient.post().uri("/detect")    //... Post 방식으로 Request, endpoint = /detect
                .contentType(MediaType.MULTIPART_FORM_DATA)    //... File 전송
                .body(BodyInserters.fromMultipartData(bodyBuilder.build()))    //...  Form Data를 요청 본문으로 설정
                .retrieve()    //...  요청을 실행하고 응답을 받음 / retrieve : 회수하다
                .bodyToMono(String.class)    //... 본분을 String 방식으로 변환
                .block();    //... 비동기처리를 동기적으로 블록해서 결과 반환

        return result;
    }
/*
1. Java Rest Controller로 Text와 Image를 비동기 방식으로 전송
2. AI Server에서 Image를 받아 객체 탐지 수행
3. AI Server에서 Image를 Base64 Encoding 문자열로 변환
4. Rest Controller에서 비동기 방식으로 Text와 Image를 변환
5. 비동기 요청 View Page에서 결과를 화면에 출력
*/

}
