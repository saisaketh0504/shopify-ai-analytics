class Api::V1::QuestionsController < ApplicationController
  def create
    store_id = params[:store_id]
    question = params[:question]

    if store_id.blank? || question.blank?
      return render json: { error: "Invalid input" }, status: 400
    end

    response = HTTParty.post(
      "http://localhost:8000/ask",
      body: {
        store_id: store_id,
        question: question
      }.to_json,
      headers: { "Content-Type" => "application/json" }
    )

    render json: response.parsed_response
  end
end
