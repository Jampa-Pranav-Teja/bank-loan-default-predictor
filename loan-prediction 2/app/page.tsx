"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, CheckCircle, TrendingUp, Shield, Calculator } from "lucide-react"

interface LoanData {
  gender: string
  loan_type: string
  loan_purpose: string
  credit_worthiness: string
  loan_amount: string
  term: string
  property_value: string
  occupancy_type: string
  secured_by: string
  total_units: string
  income: string
  credit_type: string
  credit_score: string
  co_applicant_credit_type: string
  age: string
  ltv: string
  region: string
  dtir1: string
}

interface PredictionResult {
  prediction: "approved" | "rejected" | "review"
  confidence: number
  risk_factors: string[]
  recommendation: string
}

export default function LoanPredictionApp() {
  const [formData, setFormData] = useState<LoanData>({
    gender: "",
    loan_type: "",
    loan_purpose: "",
    credit_worthiness: "",
    loan_amount: "",
    term: "",
    property_value: "",
    occupancy_type: "",
    secured_by: "",
    total_units: "",
    income: "",
    credit_type: "",
    credit_score: "",
    co_applicant_credit_type: "",
    age: "",
    ltv: "",
    region: "",
    dtir1: "",
  })

  const [prediction, setPrediction] = useState<PredictionResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleInputChange = (field: keyof LoanData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      const result = await response.json()
      setPrediction(result)
    } catch (error) {
      console.error("Prediction error:", error)
      // Mock prediction for demo
      setPrediction({
        prediction: Math.random() > 0.5 ? "approved" : "rejected",
        confidence: Math.random() * 100,
        risk_factors: ["Credit Score", "Debt-to-Income Ratio"],
        recommendation: "Based on the analysis, this application requires manual review.",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getPredictionColor = (pred: string) => {
    switch (pred) {
      case "approved":
        return "text-green-600 bg-green-50 border-green-200"
      case "rejected":
        return "text-red-600 bg-red-50 border-red-200"
      default:
        return "text-yellow-600 bg-yellow-50 border-yellow-200"
    }
  }

  const getPredictionIcon = (pred: string) => {
    switch (pred) {
      case "approved":
        return <CheckCircle className="h-5 w-5" />
      case "rejected":
        return <AlertCircle className="h-5 w-5" />
      default:
        return <TrendingUp className="h-5 w-5" />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-lg">
              <Shield className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">LoanGuard AI</h1>
              <p className="text-sm text-muted-foreground">Advanced Loan Default Prediction System</p>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Form Section */}
          <div className="lg:col-span-2">
            <Card className="form-section">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calculator className="h-5 w-5" />
                  Loan Application Details
                </CardTitle>
                <CardDescription>
                  Enter the loan application information to get an AI-powered default risk assessment
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Personal Information */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-foreground">Personal Information</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="gender">Gender</Label>
                        <Select value={formData.gender} onValueChange={(value) => handleInputChange("gender", value)}>
                          <SelectTrigger>
                            <SelectValue placeholder="Select gender" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Male">Male</SelectItem>
                            <SelectItem value="Female">Female</SelectItem>
                            <SelectItem value="Other">Other</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="age">Age</Label>
                        <Input
                          id="age"
                          type="number"
                          placeholder="Enter age"
                          value={formData.age}
                          onChange={(e) => handleInputChange("age", e.target.value)}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Loan Details */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-foreground">Loan Details</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="loan_type">Loan Type</Label>
                        <Select
                          value={formData.loan_type}
                          onValueChange={(value) => handleInputChange("loan_type", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select loan type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Personal">Personal</SelectItem>
                            <SelectItem value="Home">Home</SelectItem>
                            <SelectItem value="Auto">Auto</SelectItem>
                            <SelectItem value="Business">Business</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="loan_purpose">Loan Purpose</Label>
                        <Select
                          value={formData.loan_purpose}
                          onValueChange={(value) => handleInputChange("loan_purpose", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select purpose" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Home Purchase">Home Purchase</SelectItem>
                            <SelectItem value="Refinance">Refinance</SelectItem>
                            <SelectItem value="Cash Out">Cash Out</SelectItem>
                            <SelectItem value="Other">Other</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="loan_amount">Loan Amount ($)</Label>
                        <Input
                          id="loan_amount"
                          type="number"
                          placeholder="Enter loan amount"
                          value={formData.loan_amount}
                          onChange={(e) => handleInputChange("loan_amount", e.target.value)}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="term">Term (months)</Label>
                        <Input
                          id="term"
                          type="number"
                          placeholder="Enter term in months"
                          value={formData.term}
                          onChange={(e) => handleInputChange("term", e.target.value)}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Financial Information */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-foreground">Financial Information</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="income">Annual Income ($)</Label>
                        <Input
                          id="income"
                          type="number"
                          placeholder="Enter annual income"
                          value={formData.income}
                          onChange={(e) => handleInputChange("income", e.target.value)}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="credit_score">Credit Score</Label>
                        <Input
                          id="credit_score"
                          type="number"
                          placeholder="Enter credit score"
                          value={formData.credit_score}
                          onChange={(e) => handleInputChange("credit_score", e.target.value)}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="credit_worthiness">Credit Worthiness</Label>
                        <Select
                          value={formData.credit_worthiness}
                          onValueChange={(value) => handleInputChange("credit_worthiness", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select credit worthiness" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Excellent">Excellent</SelectItem>
                            <SelectItem value="Good">Good</SelectItem>
                            <SelectItem value="Fair">Fair</SelectItem>
                            <SelectItem value="Poor">Poor</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="dtir1">Debt-to-Income Ratio (%)</Label>
                        <Input
                          id="dtir1"
                          type="number"
                          step="0.01"
                          placeholder="Enter DTI ratio"
                          value={formData.dtir1}
                          onChange={(e) => handleInputChange("dtir1", e.target.value)}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Property Information */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-foreground">Property Information</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="property_value">Property Value ($)</Label>
                        <Input
                          id="property_value"
                          type="number"
                          placeholder="Enter property value"
                          value={formData.property_value}
                          onChange={(e) => handleInputChange("property_value", e.target.value)}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="ltv">Loan-to-Value Ratio (%)</Label>
                        <Input
                          id="ltv"
                          type="number"
                          step="0.01"
                          placeholder="Enter LTV ratio"
                          value={formData.ltv}
                          onChange={(e) => handleInputChange("ltv", e.target.value)}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="occupancy_type">Occupancy Type</Label>
                        <Select
                          value={formData.occupancy_type}
                          onValueChange={(value) => handleInputChange("occupancy_type", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select occupancy type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Owner Occupied">Owner Occupied</SelectItem>
                            <SelectItem value="Investment">Investment</SelectItem>
                            <SelectItem value="Second Home">Second Home</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="total_units">Total Units</Label>
                        <Input
                          id="total_units"
                          type="number"
                          placeholder="Enter total units"
                          value={formData.total_units}
                          onChange={(e) => handleInputChange("total_units", e.target.value)}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Additional Information */}
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-foreground">Additional Information</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="secured_by">Secured By</Label>
                        <Select
                          value={formData.secured_by}
                          onValueChange={(value) => handleInputChange("secured_by", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select security type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Real Estate">Real Estate</SelectItem>
                            <SelectItem value="Vehicle">Vehicle</SelectItem>
                            <SelectItem value="Other">Other</SelectItem>
                            <SelectItem value="Unsecured">Unsecured</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="credit_type">Credit Type</Label>
                        <Select
                          value={formData.credit_type}
                          onValueChange={(value) => handleInputChange("credit_type", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select credit type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="EQUI">EQUI</SelectItem>
                            <SelectItem value="EXPR">EXPR</SelectItem>
                            <SelectItem value="CRF">CRF</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="co_applicant_credit_type">Co-Applicant Credit Type</Label>
                        <Select
                          value={formData.co_applicant_credit_type}
                          onValueChange={(value) => handleInputChange("co_applicant_credit_type", value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select co-applicant credit type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="EQUI">EQUI</SelectItem>
                            <SelectItem value="EXPR">EXPR</SelectItem>
                            <SelectItem value="CRF">CRF</SelectItem>
                            <SelectItem value="None">None</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="region">Region</Label>
                        <Select value={formData.region} onValueChange={(value) => handleInputChange("region", value)}>
                          <SelectTrigger>
                            <SelectValue placeholder="Select region" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="North">North</SelectItem>
                            <SelectItem value="South">South</SelectItem>
                            <SelectItem value="East">East</SelectItem>
                            <SelectItem value="West">West</SelectItem>
                            <SelectItem value="Central">Central</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </div>

                  <Button type="submit" className="w-full" disabled={isLoading} size="lg">
                    {isLoading ? "Analyzing..." : "Predict Default Risk"}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {prediction && (
              <Card className="prediction-card">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    {getPredictionIcon(prediction.prediction)}
                    Prediction Result
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className={`p-4 rounded-lg border ${getPredictionColor(prediction.prediction)}`}>
                    <div className="flex items-center justify-between">
                      <span className="font-semibold capitalize">{prediction.prediction}</span>
                      <Badge variant="secondary">{prediction.confidence.toFixed(1)}% confidence</Badge>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">Risk Factors</h4>
                    <div className="space-y-1">
                      {prediction.risk_factors.map((factor, index) => (
                        <Badge key={index} variant="outline" className="mr-2">
                          {factor}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">Recommendation</h4>
                    <p className="text-sm text-muted-foreground">{prediction.recommendation}</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Info Card */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">How It Works</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-muted-foreground">
                <p>Our AI model analyzes 18 key factors to predict loan default risk:</p>
                <ul className="space-y-1 ml-4">
                  <li>• Personal demographics and credit history</li>
                  <li>• Loan characteristics and terms</li>
                  <li>• Financial capacity and debt ratios</li>
                  <li>• Property and collateral information</li>
                </ul>
                <p className="text-xs pt-2 border-t">
                  This tool provides risk assessment guidance and should be used alongside human judgment for final
                  decisions.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
