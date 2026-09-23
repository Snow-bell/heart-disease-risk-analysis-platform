-- chest_pain_type
INSERT INTO chest_pain_type (code, description) VALUES
(1, 'typical angina'),
(2, 'atypical angina'),
(3, 'non-anginal'),
(4, 'asymptomatic');

-- restecg_type
INSERT INTO restecg_type (code, description) VALUES
(0, 'normal'),
(1, 'st-t abnormality'),
(2, 'lv hypertrophy');

-- slope_type
INSERT INTO slope_type (code, description) VALUES
(1, 'upsloping'),
(2, 'flat'),
(3, 'downsloping');

-- thal_type
INSERT INTO thal_type (code, description) VALUES
(3, 'normal'),
(6, 'fixed defect'),
(7, 'reversable defect');