package com.philippeducasse.portfolio_backend.controller;

import com.philippeducasse.portfolio_backend.model.Review;
import com.philippeducasse.portfolio_backend.repository.ReviewRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/reviews")

public class ReviewController {

    @Autowired
    private ReviewRepository reviewRepository;

    @GetMapping
    public List<Review> getAllReviews(){
        return reviewRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Review> createReview(@RequestBody ReviewRequest reviewRequest){
        Review review = new Review();
        review.setContent(reviewRequest.getContent());
        review.setCreatedAt(LocalDateTime.now());
        review.setAuthor(reviewRequest.getAuthor());

        Review savedReview = reviewRepository.save(review);

        return ResponseEntity.ok(savedReview);
    }

    public static class ReviewRequest {
        private String content;
        private String author;

        public String getContent(){
            return content;
        }
        public String getAuthor(){
            return author;
        }

        public void setContent(String content) {
            this.content = content;
        }

        public void setAuthor(String author) {
            this.author = author;
        }
    }
}
