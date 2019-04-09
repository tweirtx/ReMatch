#!/usr/bin/env bash

# Clone and enter ReMatch directory
git clone https://github.com/tweirtx/ReMatch
cd ReMatch

# Install pyenv
curl https://pyenv.run | bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
echo 'export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Install Python dependencies
if [[ "$OSTYPE" == "darwin"* ]]; then
    CFLAGS="-I$(xcrun --show-sdk-path)/usr/include" pyenv install 3.7.2
else
    pyenv install 3.7.2
fi
pyenv local 3.7.2
pip install -Ur requirements.txt

# Set up postgres
if [[ "$OSTYPE" == "darwin"* ]]; then
    export PATH="/Library/PostgreSQL/11/bin:$PATH"
    psql -U postgres -f setup.sql
else
    sudo -u postgres psql -f setup.sql
fi

echo "ReMatch setup complete!"
